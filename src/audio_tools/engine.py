import sounddevice as sd
import soundfile as sf

class AudioEngine:
    def __init__(self):
        self.playing_objects = []

    def play_wav(self, file_path: str):
        try:
            data, fs = sf.read(file_path)
            sd.play(data, fs)
            self._refresh_playing_objects()
            self.playing_objects.append({"file": file_path, "status": "playing"})
        except Exception as e:
            print(f"\n[AudioEngine Error] failed to play! {file_path}: {e}")

    def wait_all(self):
        sd.wait()
        self.playing_objects.clear()

    def _refresh_playing_objects(self):
        if not sd.get_stream().active:
            self.playing_objects.clear()
