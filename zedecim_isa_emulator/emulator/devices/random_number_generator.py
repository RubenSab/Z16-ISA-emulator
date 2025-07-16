import random

class RandomNumberGenerator():
    def __init__(self):
        pass

    def get_input(self, data):
        min_bound = min(0, data)
        max_bound = max(0, data)
        return random.randint(min_bound, max_bound)