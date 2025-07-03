class Word(int):
    DEFAULT_BIT_WIDTH = 16

    def __new__(cls, value, bit_width=None):
        bit_width = bit_width or cls.DEFAULT_BIT_WIDTH
        bit_mask = (1 << bit_width) - 1
        max_value = (1 << (bit_width - 1)) - 1

        wrapped = value & bit_mask
        if wrapped > max_value:
            wrapped -= (bit_mask + 1)

        obj = super().__new__(cls, wrapped)
        obj._bit_width = bit_width
        obj._bit_mask = bit_mask
        obj._max_value = max_value
        obj._min_value = -1 * (1 << (bit_width - 1))
        return obj

    def __add__(self, other):
        return Word(int(self) + int(other), self._bit_width)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return Word(int(self) - int(other), self._bit_width)

    def __rsub__(self, other):
        return Word(int(other) - int(self), self._bit_width)

    def __mul__(self, other):
        return Word(int(self) * int(other), self._bit_width)

    def __rmul__(self, other):
        return self.__mul__(other)

    def to_hex(self):
        return f"{(int(self) & self._bit_mask):0{self._bit_width // 4}X}"

    @classmethod
    def from_bytes(cls, byte_data: bytes, byteorder='big', signed=False, bit_width=None):
        if not isinstance(byte_data, bytes):
            raise TypeError("byte_data must be of type 'bytes'")
        if len(byte_data) * 8 != (bit_width or cls.DEFAULT_BIT_WIDTH):
            raise ValueError(f"Input length does not match expected bit width: {bit_width or cls.DEFAULT_BIT_WIDTH} bits")
        value = int.from_bytes(byte_data, byteorder=byteorder, signed=signed)
        return cls(value, bit_width)

    def __str__(self):
        return self.to_hex()
