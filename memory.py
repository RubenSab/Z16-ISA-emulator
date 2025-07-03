from word import Word

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


    def store_word(self, address, content: Word):
        content = Word(content)
        if address >= self.memory_byte_size//2:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_byte_size} bytes long memory."
            )
        self.word_memory[address] = content


    def load_word(self, address):
        if address >= self.memory_byte_size//2:
            raise MemoryIndexError(
                f"word location {address} doesn't exist "
                f"inside {self.memory_byte_size} bytes long memory."
            )
        return self.word_memory[address]


    def load_file(self, filename):
        with open(filename, "rb") as f:
            byte_sequence = f.read()

        if len(byte_sequence) > self.memory_byte_size:
            raise MemoryOverflowError(
                f"Bytecode of length {len(byte_sequence)} doesn't fit "
                f"inside {self.memory_byte_size} bytes long memory."
            )

        # load two bytes (so one word) per memory location
        for i in range(0, len(byte_sequence), 2):
            self.store_word(
                content = Word.from_bytes(byte_sequence[i:i+2]),
                address = i//2
            )

    # TODO: add dump_memory(filename)

    def __repr__(self):
        return str([word.to_hex() for word in self.word_memory])
