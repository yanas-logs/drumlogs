import numpy as np

class AudioMixer:
    @staticmethod
    def mix_signals(signals):
        if not signals:
            return np.zeros(100, dtype=np.float32)

        max_length = max(len(s) for s in signals)
        mixed = np.zeros(max_length, dtype=np.float32)

        for s in signals:
            s_float = s.astype(np.float32)
            if np.max(np.abs(s_float)) > 1.0:
                s_float = s_float / 32768.0
            mixed[:len(s_float)] += s_float

        return np.clip(mixed, -1.0, 1.0).astype(np.float32)
