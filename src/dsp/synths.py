import numpy as np

class DrumSynth:
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate

    def generate_kick(self, duration=0.2, start_freq=150, end_freq=40):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        freq = np.geomspace(start_freq, end_freq, len(t))
        phase = 2 * np.pi * np.cumsum(freq) / self.sample_rate
        
        envelope = np.exp(-10 * t)
        signal = np.sin(phase) * envelope
        
        return (signal * 32767).astype(np.int16)

    def generate_snare(self, duration=0.15):
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        
        noise = np.random.uniform(-1, 1, len(t))
        
        envelope = np.exp(-15 * t)
        signal = noise * envelope
        
        return (signal * 32767).astype(np.int16)
