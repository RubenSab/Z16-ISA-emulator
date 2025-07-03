from constants import INSTRUCTIONS

class CPU:
    def __init__(self, MEMORY_BYTE_SIZE, filename=None):
        self.MEMORY_BYTE_SIZE = MEMORY_BYTE_SIZE
        self.MEMORY_COUNTER_INIT = MEMORY_BYTE_SIZE//2
        self.memory = [0 for i in range(MEMORY_BYTE_SIZE*2)]
        self.registers = [0]*16
        # implement memory, registers, program counter and memory counter as classes
        self.filename = filename
        if self.filename:
            self.load_memory(self.filename)

    def load_memory(self, filename):
        with open(filename, "rb") as f:
            byte_sequence = f.read()

        for i in range(0, len(byte_sequence), 2):
            self.memory[i//2] = byte_sequence[i:i+2]

    def fetch(self, address: int) -> str:
        first_byte = format(self.memory[address][0], '08b')
        second_byte = format(self.memory[address][1], '08b')
        return [
            first_byte[:4],
            first_byte[4:],
            second_byte[:4],
            second_byte[4:]
        ]

if __name__=='__main__':
    from assembler import Assembler
    assembler = Assembler('test')
    assembler.assemble()
    assembler.save('test_bytes')

    a = CPU(64, 'test_bytes')
    print(a.fetch(0))

