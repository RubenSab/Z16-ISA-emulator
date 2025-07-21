from zedecim_isa_emulator.emulator.word import Word
from zedecim_isa_emulator.emulator.memory.counter import Counter

class MemoryOverflowError(Exception):
    pass

class MemoryIndexError(Exception):
    pass

class InvalidMemorySize(Exception):
    pass

class Memory:
    def __init__(self, memory_byte_size):
        # Initialize memory size
        self.memory_word_size = memory_byte_size//2
        if self.memory_word_size<=0 or \
        not isinstance(self.memory_word_size, int):
            raise InvalidMemorySize(
                f"{memory_word_size} is not a valid memory size."
            )
        # Initialize memory array
        self.word_memory = [Word(0)]*(self.memory_word_size)
        # Initialize program counter to 0
        self.program_counter = Counter(self.memory_word_size, 0)
        # initialize memory counter at the middle of memory space
        self.memory_counter = Counter(
            self.memory_word_size,
            self.memory_word_size//2
        )


    def store_word(self, address, content: Word):
        content = Word(content)
        if address >= self.memory_word_size:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_byte_size//2} words long memory."
            )
        self.word_memory[int(address)] = content


    def load_word(self, address) -> Word:
        if address >= self.memory_word_size:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_word_size} words long memory."
            )
        return self.word_memory[int(address)]


    def load_memory_from(self, filename):
        with open(filename, "rb") as f:
            byte_sequence = f.read()

        if len(byte_sequence) > self.memory_word_size*2:
            raise MemoryOverflowError(
                f"Bytecode of length {len(byte_sequence)} doesn't fit "
                f"inside {self.memory_word_size} words long memory."
            )

        # load two bytes (so one word) per memory location
        for i in range(0, len(byte_sequence), 2):
            self.store_word(
                content = Word.from_bytes(byte_sequence[i:i+2]),
                address = i//2
            )

    def dump_memory_to(self, filename):
        with open(filename, "wb") as f:
            for word in self.word_memory:
                f.write(word.to_bytes())

    def str_by_base(self, base=16):
        if base not in (2, 10, 16):
            raise ValueError("Base must be 2, 10 or 16")

        # Set per-line width and word formatter based on base
        if base == 2:
            words_per_line = 4
            format_word = lambda w: f"{w.to_bin():>16}"
            format_addr = lambda i: f"0x{i:04X}"
        elif base == 10:
            words_per_line = 8
            format_word = lambda w: f"{int(w):>6}"
            format_addr = lambda i: f"{i: 4}"
        elif base == 16:
            words_per_line = 8
            format_word = lambda w: w.to_hex()
            format_addr = lambda i: f"0x{i:04X}"

        lines = []
        for i in range(0, len(self.word_memory), words_per_line):
            row = self.word_memory[i:i + words_per_line]
            row_str = " ".join(format_word(word) for word in row)
            lines.append(f"{format_addr(i)}: {row_str}")

        return "\n".join(lines)

    def __repr__(self):
        return self.str_by_base(16)
