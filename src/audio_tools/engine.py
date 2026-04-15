import simpleaudio as sa

class AudioEngine:
    def __init__(self):
        self.playing_objects = []

    def play_wav(self, file_path):
        if not file_path:
            return None
            
        try:
            wave_obj = sa.WaveObject.from_wave_file(file_path)
            play_obj = wave_obj.play()
            self.playing_objects.append(play_obj)
            return play_obj
        except Exception as e:
            print(f"Error playing sound: {e}")
            return None

    def wait_all(self):
        for play_obj in self.playing_objects:
            play_obj.wait_done()
