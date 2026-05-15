import numpy as np

class DrumSynth:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def _apply_envelope(self, signal, attack=0.01, release=0.1):
        total_samples = len(signal)
        attack_samples = int(attack * self.sample_rate)

        envelope = np.ones(total_samples)

        if attack_samples > 0:
            envelope[:attack_samples] = np.linspace(0, 1, attack_samples)

        release_indices = np.arange(total_samples)
        envelope *= np.exp(-1 * release_indices / (release * self.sample_rate))

        return signal * envelope

    def generate_kick(self, duration=0.2, f_start=150, f_end=40):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        freq = np.geomspace(f_start, f_end, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate

        signal = np.sin(phase)

        return (self._apply_envelope(signal, 0.005, 0.05) * 32767).astype(np.int16)

    def generate_snare(self, duration=0.15):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        noise = np.random.uniform(-1, 1, len(t))

        return (self._apply_envelope(noise, 0.01, 0.03) * 32767).astype(np.int16)

    def generate_hihat(self, duration=0.05):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        noise = np.random.uniform(-1, 1, len(t))

        return (self._apply_envelope(noise, 0.002, 0.01) * 20000).astype(np.int16)

    def generate_kendang(self, tone="tak"):
        if tone == "tak":
            return self.generate_snare(duration=0.12)
        elif tone == "dung":
            return self.generate_kick(duration=0.25)
        else:
            return self.generate_snare()

    def generate_saron(self, freq=440, duration=0.5):
        t = np.linspace(0, duration, int(self.sample_rate * duration))

        signal = (
            np.sin(2 * np.pi * freq * t) * 0.6 +
            np.sin(2 * np.pi * freq * 2 * t) * 0.3
        )

        return (self._apply_envelope(signal, 0.01, 0.2) * 32767).astype(np.int16)