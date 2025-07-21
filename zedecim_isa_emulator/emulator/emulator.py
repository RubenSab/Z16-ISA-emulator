from zedecim_isa_emulator.emulator.assembler import Assembler
from zedecim_isa_emulator.emulator.cpu.cpu import CPU

class Emulator:
    def __init__(self, memory_byte_size):
        """
        Initialize the Emulator with a given memory size.

        Args:
            memory_byte_size (int): The size of the memory in bytes to allocate
            for the emulator.
        """
        self.memory_byte_size = memory_byte_size
        self.cpu = CPU(self.memory_byte_size)
        self.assembler = Assembler()

    def execute_code(self, source_filename, memory_filename=None):
        """
        Assemble and execute code from a source file.

        Args:
            source_filename (str): Path to the assembly source code file.
            memory_filename (str, optional): Path to the file where memory
            state will be dumped after execution.
            If None, memory will not be dumped. Defaults to None.
        """
        # Assemble code
        self.assembler.assemble(source_filename)
        binary_filename = source_filename.split('.')[0]+'.bin'
        self.assembler.store_bytes(binary_filename)
        self.execute_bin(binary_filename, memory_filename)

    def execute_bin(self, binary_filename, memory_filename=None):
        """
        Load and execute a binary file.

        Args:
            binary_filename (str): Path to the binary file to be loaded into
            memory and executed.
            memory_filename (str, optional): Path to the file where memory
            state will be dumped after execution.
            If None, memory will not be dumped. Defaults to None.
        """
        self.cpu.load_memory_from(binary_filename)
        self.cpu.execute()
        # Dump memory
        if memory_filename:
            self.cpu.memory.dump_memory_to(memory_filename)

    def reset(self):
        """
        Reset the emulator by reinitializing the CPU and assembler with the
        original memory size.
        """
        self.__init__(self.memory_byte_size)
