from memory import Memory
from registers import Registers
from deassembler import deassemble_word
from registers import REGISTER_NAMES
from instructions import INSTRUCTIONS, INSTRUCTIONS_LIST
from counter import Counter
from word import Word

class CPU:

    def __init__(self, memory_size):
        self.INSTRUCTION_FUNCTIONS = {
            "and": self._bitwise_and,
            "or": self._bitwise_or,
            "xor": self._bitwise_xor,
            "not": self._bitwise_not,
            "sh": self._shift,
            "add": self._add,
            "sub": self._sub,
            "mul": self._mul,
            "div": self._int_div,
            "comp": self._compare,
            "li": self._load_immediate,
            "apeq": self._add_to_program_counter_if_X_is_equal_to_zero,
            "amc": self._add_to_memory_counter,
            "lw": self._load_word,
            "sw": self._store_word,
            "criio": self._custom_register_immediate_input_output,
        }
        self.memory_size = memory_size
        self.memory = Memory(memory_size)
        self.registers = Registers()
        self.program_counter = Counter(4)
        self.memory_counter = Counter(4, self.memory_size//2)
        self.exit_codes = {
            Word(int('0000', 16)): 'No instructions left to execute.',
            Word(int('1000', 16)): 'Execution completed with success.',
            Word(int('2000', 16)): 'Memory overflow error.',
            Word(int('3000', 16)): 'Invalid memory address.',
            Word(int('4000', 16)): 'Custom exit code 0x4000',
            Word(int('5000', 16)): 'Custom exit code 0x5000',
            Word(int('6000', 16)): 'Custom exit code 0x6000',
            Word(int('7000', 16)): 'Custom exit code 0x7000',
            Word(int('8000', 16)): 'Custom exit code 0x8000',
            Word(int('9000', 16)): 'Custom exit code 0x9000',
            Word(int('A000', 16)): 'Custom exit code 0xA000',
        }
        self.exit_code = None

    def load_memory_from(self, filename):
        self.memory.load_memory_from(filename)


    def execute(self):
        while True:
            # --- Instruction fetch ---
            instruction = self.memory.load_word(int(self.program_counter))
            # Every "exit code" that is not a proper one indicates that
            # the execution is still running, possibly useful for debugging.
            self.exit_code = instruction
            if self.exit_code in self.exit_codes:
                print(f"0x{self.exit_code}: {self.exit_codes[self.exit_code]}")
                break

            # --- Instruction decode ---
            parsed_instruction = deassemble_word(instruction)
            print(parsed_instruction)

            # --- Instruction execution ---
            self.execute_parsed_instruction(parsed_instruction)

            break #placeholder, program counter behaviour yet to implement
 

    def execute_parsed_instruction(self, instruction: dict):
        return instruction


    def _bitwise_and(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _bitwise_or(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _bitwise_xor(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _bitwise_not(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _shift(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _add(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _sub(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _mul(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _int_div(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _compare(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _load_immediate(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _add_to_program_counter_if_X_is_equal_to_zero(
    self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _add_to_memory_counter(
    self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _load_word(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _store_word(self, target=None, op1=None, op2=None, immediate=None):
        pass

    def _custom_register_immediate_input_output(
    self, target=None, op1=None, op2=None, immediate=None):
        pass

if __name__=='__main__':
    cpu = CPU(64)
    cpu.load_memory_from('bytes_test')
    cpu.memory.store_word(0, int('1000', 16))
    cpu.execute()
    print(cpu.memory)
