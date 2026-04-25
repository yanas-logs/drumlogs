import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import (
    AudioLoader, 
    AudioProcessor, 
    SimpleSequencer, 
    AudioEngine, 
    PatternRandomizer
)

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "audio_data")

    loader = AudioLoader(audio_folder)
    processor = AudioProcessor()
    sequencer = SimpleSequencer(bpm=125, steps=16)
    engine = AudioEngine()
    randomizer = PatternRandomizer()

    print("=== DrumLogs Algorithmic Test ===")

    categories = loader.list_categories()
    if not categories:
        return

    if "kick" in categories:
        sequencer.add_track("kick", randomizer.generate_kick_pattern())
    if "snare" in categories:
        sequencer.add_track("snare", randomizer.generate_snare_pattern())
    if "hihat" in categories:
        sequencer.add_track("hihat", randomizer.generate_hihat_pattern(density=0.7))

    step_duration = sequencer.get_step_duration()

    try:
        for loop in range(4):
            print(f"\nLoop {loop + 1}")
            for step in range(sequencer.steps):
                active_tracks = sequencer.get_active_steps(step)
                for track in active_tracks:
                    samples = loader.get_sample(track)
                    if samples:
                        sample_path = list(samples.values())[0]
                        engine.play_wav(sample_path)
                time.sleep(step_duration)
    except KeyboardInterrupt:
        print("\nExit.")

if __name__ == "__main__":
    main()
