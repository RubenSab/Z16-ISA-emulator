class Counter:
    def __init__(self, byte_size, value=0):
        self.max_value = 2**(byte_size*8)
        self.value = value % self.max_value  # ensure initial value is wrapped

    def __iadd__(self, offset):
        self.value = (self.value + offset) % self.max_value
        return self

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)

    # Comparison methods:

    def __eq__(self, other):
        if isinstance(other, Counter):
            return self.value == other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, Counter):
            return self.value < other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Counter):
            return self.value <= other.value
        return self.value <= other

    def __gt__(self, other):
        if isinstance(other, Counter):
            return self.value > other.value
        return self.value > other

    def __ge__(self, other):
        if isinstance(other, Counter):
            return self.value >= other.value
        return self.value >= other

    def __ne__(self, other):
        if isinstance(other, Counter):
            return self.value != other.value
        return self.value != other
