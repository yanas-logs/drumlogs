import os
import wave
import contextlib

class AudioProcessor:
    @staticmethod
    def get_duration(file_path):
        if not os.path.exists(file_path):
            return 0.0
        
        try:
            with contextlib.closing(wave.open(file_path, 'r')) as f:
                frames = f.getnframes()
                rate = f.getframerate()
                return frames / float(rate)
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return 0.0

    @staticmethod
    def get_info(file_path):
        try:
            with contextlib.closing(wave.open(file_path, 'r')) as f:
                return {
                    "channels": f.getnchannels(),
                    "sample_width": f.getsampwidth(),
                    "frame_rate": f.getframerate(),
                    "n_frames": f.getnframes()
                }
        except Exception:
            return {}
