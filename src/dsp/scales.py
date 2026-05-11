import numpy as np

class ScaleMapper:
    SCALES = {
        "slendro": [262, 294, 330, 392, 440],
        "pelog": [262, 277, 311, 349, 392, 415, 466],
        "chromatic": [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88]
    }

    def get_freq(self, scale_name, note_index):
        scale = self.SCALES.get(scale_name, self.SCALES["chromatic"])
        return scale[note_index % len(scale)]
