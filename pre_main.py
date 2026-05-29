import os
import sys
import time
import random
from datetime import datetime
import numpy as np
import sounddevice as sd

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from audio_tools import SimpleSequencer, ConfigManager, TerminalVisualizer
from dsp import DrumSynth, AudioEffects, ScaleMapper, AudioMixer

def get_time_based_bpm_bounds() -> tuple[float, float, str]:
    current_hour = datetime.now().hour
    if 6 <= current_hour < 12:
        return 76.0, 84.0, "Morning Focus"
    elif 12 <= current_hour < 18:
        return 80.0, 88.0, "Afternoon Energy"
    elif 18 <= current_hour < 24:
        return 72.0, 78.0, "Evening Chill"
    else:
        return 65.0, 72.0, "Late Night Ambient"

def smooth_bpm_drift(current_bpm: float, min_bpm: float, max_bpm: float) -> float:
    drift = random.uniform(-0.5, 0.5)
    new_bpm = current_bpm + drift
    return max(min_bpm, min(max_bpm, new_bpm))

def generate_dynamic_pattern(total_steps: int) -> list[int]:
    base_pattern = [1, 0, 0, 0]
    pattern = []
    while len(pattern) < total_steps:
        pattern.extend(base_pattern)
    return pattern[:total_steps]

def main():
    config = ConfigManager()
    synth = DrumSynth()
    fx = AudioEffects()
    mapper = ScaleMapper()
    mixer = AudioMixer()
    ui = TerminalVisualizer()

    total_steps = random.choice([16, 32, 64])
    min_bpm, max_bpm, time_zone_name = get_time_based_bpm_bounds()
    current_bpm = random.uniform(min_bpm, max_bpm)

    sequencer = SimpleSequencer(bpm=current_bpm, steps=total_steps)
    kendang_tak_pattern = generate_dynamic_pattern(total_steps)
    kendang_dung_pattern = [0 if i % 4 == 0 else (1 if i % 4 == 2 else 0) for i in range(total_steps)]

    sequencer.add_track("kendang_tak", kendang_tak_pattern)
    sequencer.add_track("kendang_dung", kendang_dung_pattern)

    sounds = {
        "kendang_tak": fx.apply_gain(synth.generate_kendang(tone="tak"), 0.8),
        "kendang_dung": fx.apply_gain(synth.generate_kendang(tone="dung"), 0.9)
    }

    saron_notes = {}
    for i in range(5):
        freq = mapper.get_freq("slendro", i)
        raw_saron = synth.generate_saron(freq=freq)
        saron_fx = fx.apply_delay(raw_saron, delay_samples=6000, feedback=0.4)
        saron_notes[i] = fx.apply_gain(saron_fx, 0.5)

    try:
        print("DrumLogs Engine | Advanced Time-Aware Randomizer")
        print(f"Structure: {total_steps} Steps | Mode: {time_zone_name}")
        print("-" * 60)

        for loop in range(4):
            min_bpm, max_bpm, time_zone_name = get_time_based_bpm_bounds()
            current_bpm = smooth_bpm_drift(current_bpm, min_bpm, max_bpm)
            
            sequencer.bpm = current_bpm
            step_duration = 15.0 / current_bpm

            for step in range(sequencer.steps):
                active_tracks = sequencer.get_active_steps(step)
                step_signals = []

                if kendang_tak_pattern[step] == 1:
                    step_signals.append(sounds["kendang_tak"])
                if kendang_dung_pattern[step] == 1:
                    step_signals.append(sounds["kendang_dung"])

                note_idx = step % 5
                if step % 2 == 0:
                    step_signals.append(saron_notes[note_idx])
                    active_tracks.append("saron")

                ui.render(step, total_steps, active_tracks)
                print(f"\r[Zone: {time_zone_name}] Loop: {loop + 1}/4 | Step: {step + 1:02d}/{total_steps} | BPM: {current_bpm:.2f} ", end="")
                sys.stdout.flush()

                if step_signals:
                    mixed_buffer = mixer.mix_signals(step_signals)
                    sd.play(mixed_buffer, 44100)

                time.sleep(step_duration)

        print("\n" + "-" * 60 + "\nPlayback finished.")
    except KeyboardInterrupt:
        print("\nProcess terminated.")

if __name__ == "__main__":
    main()
