from assembler import Assembler
from cpu import CPU

class Emulator:

    def __init__(self, memory_byte_size):
        self.cpu = CPU(memory_byte_size)
        self.assembler = Assembler()

    def emulate(self, source_filename):
        # Assemble code
        self.assembler.assemble(source_filename)
        binary_filename = source_filename.split('.')[0]+'.bin'
        self.assembler.store_bytes(binary_filename)

        # Execute binary
        self.cpu.load_memory_from(binary_filename)
        self.cpu.execute()

        # Display result for debugging
        self.display_state()

    def display_state(self):
        print(self.cpu.memory)
        print(self.cpu.registers)
        print('memory counter:', self.cpu.memory.memory_counter)
        print('program counter:', self.cpu.memory.program_counter)
        print('exit code:', self.cpu.exit_code_string)
