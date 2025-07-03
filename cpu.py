from memory import Memory
from registers import Registers
from deassembler import deassemble_word
from registers import REGISTER_NAMES
from instructions import INSTRUCTIONS, INSTRUCTIONS_LIST
from counter import Counter

class CPU:
    def __init__(self, memory_size):
        self.memory_size = memory_size
        self.memory = Memory(memory_size)
        self.registers = Registers()
        self.program_counter = Counter(4)
        self.memory_counter = Counter(4, self.memory_size//2)


    def load_memory_from(self, filename):
        self.memory.load_memory_from(filename)


    def execute(self):
        while True:
            # Instruction fetch
            instruction = self.memory.read_word(int(self.program_counter))

            # Instruction decode
            try:
                parsed_instruction = deassemble_word(instruction)
            except:
                break

            # Instruction execution
            self.execute_parsed_instruction(parsed_instruction)

            break #placeholder, program counter behaviour yet to implement


    def execute_parsed_instruction(self, instruction: dict):
        return instruction


if __name__=='__main__':
    cpu = CPU(64)
    cpu.load_memory_from('bytes_test')
    cpu.execute()
    print(cpu.memory)
