import math

class Word(int):
    DEFAULT_BIT_WIDTH = 16

    def __new__(cls, value, bit_width=None):
        bit_width = bit_width or cls.DEFAULT_BIT_WIDTH
        bit_mask = (1 << bit_width) - 1
        max_signed = (1 << (bit_width - 1)) - 1
        min_signed = -1 * (1 << (bit_width - 1))

        wrapped = value & bit_mask
        if wrapped > max_signed:
            wrapped -= (bit_mask + 1)

        obj = super().__new__(cls, wrapped)
        obj._bit_width = bit_width
        obj._bit_mask = bit_mask
        obj._max_value = max_signed
        obj._min_value = min_signed
        return obj

    def __binary_op(self, other, op):
        return Word(op(int(self), int(other)), self._bit_width)

    def __add__(self, other): return self.__binary_op(other, lambda a, b: a + b)
    def __radd__(self, other): return self.__add__(other)
    def __sub__(self, other): return self.__binary_op(other, lambda a, b: a - b)
    def __rsub__(self, other): return self.__binary_op(other, lambda a, b: b - a)
    def __mul__(self, other): return self.__binary_op(other, lambda a, b: a * b)
    def __rmul__(self, other): return self.__mul__(other)

    @classmethod
    def from_bytes(cls, byte_data: bytes, byteorder='big', signed=False, bit_width=None):
        if not isinstance(byte_data, bytes):
            raise TypeError("byte_data must be of type 'bytes'")
        bit_width = bit_width or cls.DEFAULT_BIT_WIDTH
        expected_length = math.ceil(bit_width / 8)
        if len(byte_data) != expected_length:
            raise ValueError(f"Input length ({len(byte_data)} bytes) does not match expected bit width ({bit_width} bits)")
        value = int.from_bytes(byte_data, byteorder=byteorder, signed=signed)
        return cls(value, bit_width)

    def to_bytes(self, byteorder='big', signed=False):
        byte_length = math.ceil(self._bit_width / 8)
        raw_value = int(self) if signed else (int(self) & self._bit_mask)
        return raw_value.to_bytes(byte_length, byteorder=byteorder, signed=signed)

    def to_hex(self):
        hex_digits = math.ceil(self._bit_width / 4)
        return f"{int(self) & self._bit_mask:0{hex_digits}X}"

    def __str__(self):
        return self.to_hex()

    def str_by_base(self, base):
        if base not in (10, 16):
            raise ValueError("Base must be 10 or 16")
        if base == 16:
            return str(f"0x{self.to_hex()}")
        elif base == 10:
            return int(self)

    def __repr__(self):
        return self.str_by_base(16)
