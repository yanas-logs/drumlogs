import os
import sys
import time
import numpy as np
import simpleaudio as sa

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import SimpleSequencer, ConfigManager
from dsp import DrumSynth, AudioEffects

def main():
    config = ConfigManager()
    synth = DrumSynth()
    fx = AudioEffects()
    
    steps = config.get("steps")
    bpm = config.get("bpm")
    sequencer = SimpleSequencer(bpm=bpm, steps=steps)

    sequencer.add_track("kendang_tak",  [1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0])
    sequencer.add_track("kendang_dung", [0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0])
    sequencer.add_track("saron",        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0])

    raw_saron = synth.generate_saron(freq=392.0)
    saron_fx = fx.apply_delay(raw_saron, delay_samples=6000, feedback=0.4)

    sounds = {
        "kendang_tak": fx.apply_gain(synth.generate_kendang(tone="tak"), 0.8),
        "kendang_dung": fx.apply_gain(synth.generate_kendang(tone="dung"), 0.9),
        "saron": fx.apply_gain(saron_fx, 0.6)
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
