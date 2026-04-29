import os
import sys
import time

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import (
    AudioLoader, 
    AudioProcessor, 
    SimpleSequencer, 
    AudioEngine, 
    PatternRandomizer,
    AudioLogger
)

def main():
    log = AudioLogger()
    log.info("Starting DrumLogs System")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    audio_folder = os.path.join(base_dir, "audio_data")

    loader = AudioLoader(audio_folder)
    sequencer = SimpleSequencer(bpm=120, steps=16)
    engine = AudioEngine()
    randomizer = PatternRandomizer()

    categories = loader.list_categories()
    if not categories:
        log.error("No audio categories found in audio_data/")
        return

    log.info(f"Categories loaded: {categories}")

    if "kick" in categories:
        sequencer.add_track("kick", randomizer.generate_kick_pattern())
    
    step_duration = sequencer.get_step_duration()

    try:
        log.info("Beginning playback loop")
        for _ in range(2):
            for step in range(sequencer.steps):
                active = sequencer.get_active_steps(step)
                for track in active:
                    samples = loader.get_sample(track)
                    if samples:
                        path = list(samples.values())[0]
                        engine.play_wav(path)
                time.sleep(step_duration)
    except KeyboardInterrupt:
        log.info("System stopped by user")

if __name__ == "__main__":
    main()
