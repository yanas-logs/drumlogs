import os
import sys
import time
import numpy as np
import simpleaudio as sa

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import SimpleSequencer, ConfigManager
from dsp import DrumSynth

def main():
    config = ConfigManager()
    synth = DrumSynth()
    sequencer = SimpleSequencer(bpm=config.get("bpm"), steps=8)

    sequencer.add_track("kick", [1, 0, 1, 0, 1, 0, 1, 0])
    sequencer.add_track("snare", [0, 0, 1, 0, 0, 0, 1, 0])

    sounds = {
        "kick": synth.generate_kick(),
        "snare": synth.generate_snare()
    }

    step_duration = sequencer.get_step_duration()

    try:
        print("Playing Synthesized Drums (DSP Mode)...")
        for _ in range(4):
            for step in range(sequencer.steps):
                active = sequencer.get_active_steps(step)
                for track in active:
                    if track in sounds:
                        sa.play_buffer(sounds[track], 1, 2, 44100)
                time.sleep(step_duration)
    except KeyboardInterrupt:
        print("\nExit.")

if __name__ == "__main__":
    main()
