from assembler import Assembler
from cpu import CPU
from word import Word
import sys

class Emulator:
    def __init__(self, memory_byte_size, print_base = 16):
        self.memory_byte_size = memory_byte_size
        self.cpu = CPU(self.memory_byte_size, print_base)
        self.assembler = Assembler()

    def execute_code(self, source_filename, memory_filename=None):
        # Assemble code
        self.assembler.assemble(source_filename)
        binary_filename = source_filename.split('.')[0]+'.bin'
        self.assembler.store_bytes(binary_filename)
        self.execute_bin(binary_filename, memory_filename)

    def execute_bin(self, binary_filename, memory_filename=None):
        self.cpu.load_memory_from(binary_filename)
        self.cpu.execute()
        self.cpu.halt_and_display()
        # Dump memory
        if memory_filename:
            self.cpu.memory.dump_memory_to(memory_filename)
        # Reset emulator
        self.reset()

    def reset(self):
        self.__init__(self.memory_byte_size)


if __name__=='__main__':
    memory_byte_size = int(sys.argv[1])
    code_filename = sys.argv[2]
    print_base = int(sys.argv[3]) if len(sys.argv) > 3 else 16
    emulator = Emulator(
        memory_byte_size,
        print_base # used for printing the CPU state at the end, optional
    )
    emulator.execute_code(sys.argv[2])
