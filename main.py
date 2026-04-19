import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import AudioLoader, AudioProcessor, SimpleSequencer, AudioEngine

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "audio_data")

    loader = AudioLoader(audio_folder)
    processor = AudioProcessor()
    sequencer = SimpleSequencer(bpm=120, steps=8)
    engine = AudioEngine()

    print("=== DrumLogs System Test ===")

    categories = loader.list_categories()
    if not categories:
        print("No audio categories found.")
        return

    kick_pattern = [1, 0, 1, 0, 1, 0, 1, 0]
    snare_pattern = [0, 0, 1, 0, 0, 0, 1, 0]

    if "kick" in categories:
        sequencer.add_track("kick", kick_pattern)
    if "snare" in categories:
        sequencer.add_track("snare", snare_pattern)

    step_duration = sequencer.get_step_duration()

    print(f"Playing Sequence at {sequencer.bpm} BPM...")
    
    try:
        for loop in range(2):
            for step in range(sequencer.steps):
                active_tracks = sequencer.get_active_steps(step)
                
                for track in active_tracks:
                    samples = loader.get_sample(track)
                    if samples:
                        sample_path = list(samples.values())[0]
                        engine.play_wav(sample_path)
                        
                        info = processor.get_info(sample_path)
                        print(f"Step {step} | {track} | {info.get('frame_rate')}Hz")
                
                time.sleep(step_duration)
    except KeyboardInterrupt:
        print("\nPlayback stopped.")

if __name__ == "__main__":
    main()
