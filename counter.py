from word import Word

class Counter:
    def __init__(self, max_address, value=0):
        self.bit_width = max_address.bit_length()-1
        self.max_value = max_address
        self.value = Word(value, self.bit_width)

    def __add__(self, offset):
        return Counter(self.max_value, self.value + offset)

    def __iadd__(self, offset):
        self.value += offset
        return self

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    # Comparison methods:

    def __eq__(self, other):
        return self.value == (other.value if isinstance(other, Counter) else other)

    def __lt__(self, other):
        return self.value < (other.value if isinstance(other, Counter) else other)

    def __le__(self, other):
        return self.value <= (other.value if isinstance(other, Counter) else other)

    def __gt__(self, other):
        return self.value > (other.value if isinstance(other, Counter) else other)

    def __ge__(self, other):
        return self.value >= (other.value if isinstance(other, Counter) else other)

    def __ne__(self, other):
        return self.value != (other.value if isinstance(other, Counter) else other)
