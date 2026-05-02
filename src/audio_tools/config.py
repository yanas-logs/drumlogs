import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        self.config_file = config_file
        self.settings = {
            "bpm": 120,
            "steps": 16,
            "audio_dir": "audio_data",
            "log_file": "drumlogs.log"
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"Error loading config: {e}")

    def get(self, key):
        return self.settings.get(key)
