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
    
    steps = config.get("steps")
    bpm = config.get("bpm")
    sequencer = SimpleSequencer(bpm=bpm, steps=steps)

    sequencer.add_track("kick",  [1, 0, 0, 0, 1, 0, 0, 0])
    sequencer.add_track("snare", [0, 0, 0, 0, 1, 0, 0, 0])
    sequencer.add_track("hihat", [1, 1, 1, 1, 1, 1, 1, 1])

    sounds = {
        "kick": synth.generate_kick(),
        "snare": synth.generate_snare(),
        "hihat": synth.generate_hihat()
    }

    step_duration = sequencer.get_step_duration()

    try:
        print(f"DrumLogs DSP Engine | BPM: {bpm} | Steps: {steps}")
        for loop in range(4):
            for step in range(sequencer.steps):
                active_tracks = sequencer.get_active_steps(step)
                for track in active_tracks:
                    if track in sounds:
                        sa.play_buffer(sounds[track], 1, 2, 44100)
                time.sleep(step_duration)
    except KeyboardInterrupt:
        print("\nProcess terminated.")

if __name__ == "__main__":
    main()
