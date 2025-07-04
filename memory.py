import math
from word import Word
from counter import Counter

class MemoryOverflowError(Exception):
    pass

class MemoryIndexError(Exception):
    pass

class InvalidMemorySize(Exception):
    pass

class Memory:
    def __init__(self, memory_byte_size):
        if memory_byte_size%2==1 or memory_byte_size<=0 \
        or not isinstance(memory_byte_size, int):
            raise InvalidMemorySize(
                f"{memory_byte_size} is not a valid memory size."
            )
        self.memory_byte_size = memory_byte_size
        self.word_memory = [Word(0)]*(self.memory_byte_size//2)
        self.counter_byte_size = 1
        # Initialize program counter to 0
        self.program_counter = Counter(self.counter_byte_size, 0)
        # initialize memory counter in the middle of memory space
        self.memory_counter = Counter(
            self.counter_byte_size,
            self.counter_byte_size//2
        )


    def store_word(self, address, content: Word):
        content = Word(content)
        if address >= self.memory_byte_size//2:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_byte_size//2} words long memory."
            )
        self.word_memory[int(address)] = content


    def load_word(self, address) -> Word:
        if address >= self.memory_byte_size//2:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_byte_size//2} words long memory."
            )
        return self.word_memory[int(address)]


    def load_memory_from(self, filename):
        with open(filename, "rb") as f:
            byte_sequence = f.read()

        if len(byte_sequence) > self.memory_byte_size:
            raise MemoryOverflowError(
                f"Bytecode of length {len(byte_sequence)} doesn't fit "
                f"inside {self.memory_byte_size//2} words long memory."
            )

        # load two bytes (so one word) per memory location
        for i in range(0, len(byte_sequence), 2):
            self.store_word(
                content = Word.from_bytes(byte_sequence[i:i+2]),
                address = i//2
            )


    def __repr__(self):
        lines = []
        for i in range(0, len(self.word_memory), 8):
            # Address of the first word in the row, as hex
            addr = f"{i:04X}"
            # Slice 8 words for this row and convert each to hex string
            row_words = self.word_memory[i:i+8]
            row_str = " ".join(word.to_hex() for word in row_words)
            lines.append(f"{addr}: {row_str}")
        return "\n".join(lines)
