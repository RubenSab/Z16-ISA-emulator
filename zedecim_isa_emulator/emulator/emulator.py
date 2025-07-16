from emulator.assembler import Assembler
from emulator.cpu.cpu import CPU

class Emulator:
    def __init__(self, memory_byte_size):
        self.memory_byte_size = memory_byte_size
        self.cpu = CPU(self.memory_byte_size)
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
        # Dump memory
        if memory_filename:
            self.cpu.memory.dump_memory_to(memory_filename)

    def reset(self):
        self.__init__(self.memory_byte_size)