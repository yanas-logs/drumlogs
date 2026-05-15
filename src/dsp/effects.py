import numpy as np

class AudioEffects:
    @staticmethod
    def apply_gain(signal, volume=0.5):
        return (signal * volume).astype(np.int16)

    @staticmethod
    def apply_delay(signal, delay_samples=4410, feedback=0.3):
        output = np.array(signal, dtype=np.float32)
        delay_part = np.zeros(len(signal) + delay_samples, dtype=np.float32)
        delay_part[delay_samples:] = signal * feedback
        
        output += delay_part[:len(signal)]
        return np.clip(output, -32768, 32767).astype(np.int16)
