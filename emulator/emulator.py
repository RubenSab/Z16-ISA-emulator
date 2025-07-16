from emulator.assembler import Assembler
from emulator.cpu.cpu import CPU
import sys

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


if __name__=='__main__':
    # Get execution settings
    memory_byte_size = int(sys.argv[1])
    code_filename = sys.argv[2]
    # Execute code
    emulator = Emulator(memory_byte_size)
    emulator.execute_code(sys.argv[2])
    # Print CPU state
    numbers_base = int(sys.argv[3]) if len(sys.argv) > 3 else None
    if numbers_base:
        emulator.cpu.display_state(numbers_base)
    # Store input/output history
    history_file = sys.argv[4] if len(sys.argv) > 4 else None
    if history_file:
        emulator.cpu.piu.console.export_history(history_file)
    # Reset emulator
    emulator.reset()