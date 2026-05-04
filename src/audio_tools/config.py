import json
import os

class ConfigManager:
    def __init__(self, config_name="config.json"):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.config_path = os.path.join(self.root_dir, "configs", config_name)
        self.settings = {
            "bpm": 100,
            "steps": 16,
            "audio_dir": "audio_data",
            "log_file": "drumlogs.log"
        }
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"Error loading config from {self.config_path}: {e}")

    def get(self, key):
        return self.settings.get(key)
