import random
from zedecim_isa_emulator.emulator.word import Word

class RandomNumberGenerator:
    def __init__(self):
        pass

    def get_input(self):
        min_bound = -32768
        max_bound = 32767
        return random.randint(min_bound, max_bound)