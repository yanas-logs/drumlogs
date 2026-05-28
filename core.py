import time
from dataclasses import dataclass
import numpy as np
import simpleaudio as sa


@dataclass(frozen=True)
def TimeSignature:
    beats_per_bar: int = 4
    note_value: int = 4


class AudioTimeProvider:
    def __init__(self, bpm: float, time_signature: TimeSignature = TimeSignature()):
        self._bpm = bpm
        self._time_signature = time_signature
        self._update_intervals()

    @property
    def bpm(self) -> float:
        return self._bpm

    @bpm.setter
    def bpm(self, new_bpm: float) -> None:
        if new_bpm <= 0:
            raise ValueError("BPM must be greater than zero.")
        self._bpm = new_bpm
        self._update_intervals()

    def _update_intervals(self) -> None:
        self._beat_duration = 60.0 / self._bpm
        self._step_16th_duration = self._beat_duration / 4

    def get_beat_duration(self) -> float:
        return self._beat_duration

    def get_step_duration(self) -> float:
        return self._step_16th_duration


class AudioEngine:
    def __init__(self, time_provider: AudioTimeProvider):
        self.time_provider = time_provider
        self._is_running = False

    def mix_samples(self, samples: list[np.ndarray]) -> np.ndarray:
        if not samples:
            return np.array([], dtype=np.int16)
        
        max_length = max(len(s) for s in samples)
        mixed = np.zeros(max_length, dtype=np.float32)
        
        for sample in samples:
            mixed[:len(sample)] += sample.astype(np.float32)
            
        mixed = np.clip(mixed, -32768, 32767)
        return mixed.astype(np.int16)

    def play_raw(self, audio_data: np.ndarray, sample_rate: int = 44100) -> sa.PlayObject:
        return sa.play_buffer(audio_data, 1, 2, sample_rate)

    def start_loop(self, tick_callback) -> None:
        self._is_running = True
        while self._is_running:
            start_time = time.perf_counter()
            
            tick_callback()
            
            interval = self.time_provider.get_step_duration()
            elapsed = time.perf_counter() - start_time
            sleep_time = max(0.0, interval - elapsed)
            time.sleep(sleep_time)

    def stop_loop(self) -> None:
        self._is_running = False
