import numpy as np

class AudioMixer:
    @staticmethod
    def mix_signals(signals):
        if not signals:
            return np.zeros(100, dtype=np.int16)
        
        max_length = max(len(s) for s in signals)
        mixed = np.zeros(max_length, dtype=np.float32)
        
        for s in signals:
            mixed[:len(s)] += s
            
        return np.clip(mixed, -32768, 32767).astype(np.int16)
