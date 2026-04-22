import random

class PatternRandomizer:
    @staticmethod
    def generate_kick_pattern(steps=16):
        pattern = [0] * steps
        for i in range(0, steps, 4):
            pattern[i] = 1
        for i in range(steps):
            if i % 4 != 0 and random.random() > 0.8:
                pattern[i] = 1
        return pattern

    @staticmethod
    def generate_snare_pattern(steps=16):
        pattern = [0] * steps
        for i in range(4, steps, 8):
            pattern[i] = 1
        return pattern

    @staticmethod
    def generate_hihat_pattern(steps=16, density=0.5):
        return [1 if random.random() < density else 0 for _ in range(steps)]
