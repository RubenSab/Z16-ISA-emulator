class Counter:
    def __init__(self, byte_size, value=0):
        self.max_value = 2**(byte_size*8)
        self.value = value

    def __iadd__(self, offset):
        self.value = self.value+offset % self.max_value
        return self.value

    def __int__(self):
        return int(self.value)

    def __str__(self):
        return str(self.value)
