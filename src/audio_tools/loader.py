import os
from pathlib import Path

class AudioLoader:
    def __init__(self, base_path):
        self.base_path = Path(base_path)
        self.samples = {}
        self.refresh()

    def refresh(self):
        """Dynamically scan audio folders."""
        if not self.base_path.exists():
            return

        self.samples = {}
        for category_dir in self.base_path.iterdir():
            if category_dir.is_dir():
                category_name = category_dir.name
                self.samples[category_name] = {}
                for audio_file in category_dir.glob("*.wav"):
                    self.samples[category_name][audio_file.stem] = str(audio_file.absolute())

    def get_sample(self, category, name=None):
        if category not in self.samples:
            return None
        return self.samples[category].get(name) if name else self.samples[category]

    def list_categories(self):
        return list(self.samples.keys())