import os
import sys
import time
import json
import random
from datetime import datetime
import numpy as np
import sounddevice as sd

sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))
from audio_tools import SimpleSequencer, ConfigManager, TerminalVisualizer
from dsp import ConfigurableSynth, AudioEffects, AudioMixer

def get_time_based_bpm_bounds() -> tuple[float, float, str]:
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return 76.0, 84.0, "Morning Focus"
    elif 12 <= current_hour < 18:
        return 80.0, 88.0, "Afternoon Energy"
    elif 18 <= current_hour < 24:
        return 72.0, 78.0, "Evening Chill"
    else:
        return 65.0, 72.0, "Late Night Ambient"

def smooth_bpm_drift(current_bpm: float, min_bpm: float, max_bpm: float) -> float:
    drift = random.uniform(-0.3, 0.3)
    new_bpm = current_bpm + drift
    return max(min_bpm, min(max_bpm, new_bpm))

def generate_lofi_kit_pattern(total_steps: int) -> tuple[list[int], list[int], list[int]]:
    kick_pattern = []
    snare_pattern = []
    hihat_pattern = []
    for i in range(total_steps):
        step_pos = i % 16
        if step_pos == 0:
            kick_pattern.append(1)
        elif step_pos == 8 and random.random() > 0.2:
            kick_pattern.append(1)
        elif step_pos == 11 and random.random() > 0.5:
            kick_pattern.append(1)
        else:
            kick_pattern.append(0)

        if step_pos in [4, 12]:
            snare_pattern.append(1)
        else:
            snare_pattern.append(0)

        if step_pos % 2 == 0:
            hihat_pattern.append(1 if random.random() > 0.1 else 0)
        else:
            hihat_pattern.append(1 if random.random() > 0.7 else 0)
    return kick_pattern, snare_pattern, hihat_pattern

def generate_vinyl_crackle(duration_samples: int, crackle_density: float = 0.0002) -> np.ndarray:
    hiss = np.random.normal(0, 0.005, duration_samples)
    crackle = np.zeros(duration_samples)
    impulse_locations = np.random.random(duration_samples) < crackle_density
    crackle[impulse_locations] = np.random.uniform(0.1, 0.3, np.sum(impulse_locations))
    crackle = np.convolve(crackle, np.exp(-np.linspace(0, 4, 15)), mode='same')
    return (hiss + crackle).astype(np.float32)

def main():
    config_path = os.path.join(os.path.dirname(__file__), "configs", "config.json")
    try:
        with open(config_path, "r") as f:
            config_data = json.load(f)
    except Exception:
        config_data = {}
    inst_params = config_data.get("instruments", {})
    synth = ConfigurableSynth()
    fx = AudioEffects()
    mixer = AudioMixer()
    ui = TerminalVisualizer()
    if not inst_params or "kick" not in inst_params:
        inst_params = {
            "kick": {"start_freq": 120.0, "end_freq": 40.0, "duration": 0.18, "wave_type": "sine"},
            "snare": {"start_freq": 260.0, "end_freq": 120.0, "duration": 0.15, "wave_type": "triangle", "noise_mix": 0.4},
            "hihat": {"start_freq": 12000.0, "end_freq": 10000.0, "duration": 0.03, "wave_type": "noise"}
        }
    total_steps = config_data.get("steps", 16)
    min_bpm, max_bpm, time_zone_name = get_time_based_bpm_bounds()
    current_bpm = config_data.get("bpm", 80)
    kick_p, snare_p, hihat_p = generate_lofi_kit_pattern(total_steps)
    sequencer = SimpleSequencer(bpm=current_bpm, steps=total_steps)
    sequencer.add_track("kick", kick_p)
    sequencer.add_track("snare", snare_p)
    sequencer.add_track("hihat", hihat_p)
    kick_node = fx.apply_gain(synth.generate_instrument(inst_params["kick"]), 1.3).astype(np.float32)
    snare_node = fx.apply_gain(synth.generate_instrument(inst_params["snare"]), 0.85).astype(np.float32)
    hihat_node = fx.apply_gain(synth.generate_instrument(inst_params["hihat"]), 0.25).astype(np.float32)
    try:
        print("DrumLogs Engine | Prototype 3 Active")
        print("-" * 60)
        sample_rate = 44100
        for loop in range(4):
            min_bpm, max_bpm, time_zone_name = get_time_based_bpm_bounds()
            current_bpm = smooth_bpm_drift(current_bpm, min_bpm, max_bpm)
            step_duration = 15.0 / current_bpm
            samples_per_step = int(sample_rate * step_duration)
            for step in range(total_steps):
                active_tracks = []
                step_signals = []
                if kick_p[step] == 1:
                    step_signals.append(kick_node)
                    active_tracks.append("kick")
                if snare_p[step] == 1:
                    step_signals.append(snare_node)
                    active_tracks.append("snare")
                if hihat_p[step] == 1:
                    step_signals.append(hihat_node)
                    active_tracks.append("hihat")
                ui.render(step, total_steps, active_tracks)
                print(f"\r[Zone: {time_zone_name}] Loop: {loop + 1}/4 | Step: {step + 1:02d}/{total_steps} | BPM: {current_bpm:.2f} ", end="")
                sys.stdout.flush()
                vinyl_noise = generate_vinyl_crackle(samples_per_step, crackle_density=0.0002)
                vinyl_noise = fx.apply_gain(vinyl_noise, 0.03)
                final_buffer = vinyl_noise.astype(np.float32).copy()
                if step_signals:
                    mixed_drums = mixer.mix_signals(step_signals).astype(np.float32)
                    length = min(len(final_buffer), len(mixed_drums))
                    final_buffer[:length] += mixed_drums[:length]
                final_buffer = np.clip(final_buffer, -1.0, 1.0)
                sd.play(final_buffer, sample_rate)
                time.sleep(step_duration)
        sd.wait()
        print("\nPlayback finished.")
    except KeyboardInterrupt:
        sd.stop()
        print("\nProcess terminated.")

if __name__ == "__main__":
    main()
