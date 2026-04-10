class SimpleSequencer:
    def __init__(self, bpm=120, steps=16):
        self.bpm = bpm
        self.steps = steps
        self.tracks = {}

    def add_track(self, instrument_name, pattern):
        if len(pattern) != self.steps:
            raise ValueError(f"Pattern must be {self.steps} steps long")
        self.tracks[instrument_name] = pattern

    def get_active_steps(self, step_index):
        active_instruments = []
        for inst, pattern in self.tracks.items():
            if pattern[step_index] == 1:
                active_instruments.append(inst)
        return active_instruments

    def set_bpm(self, bpm):
        self.bpm = bpm

    def get_step_duration(self):
        return (60 / self.bpm) / 4
