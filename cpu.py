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
            "amc": self._add_to_memory_counter,
            "lw": self._load_word,
            "sw": self._store_word,
            "criio": self._custom_register_immediate_input_output,
            "apceq": self._add_to_program_counter_if_X_is_equal_to_zero,
        }
        self.memory_size = memory_size
        self.memory = Memory(memory_size)
        self.registers = Registers()
        self.program_counter = Counter(4)
        self.memory_counter = Counter(4, self.memory_size//2)
        self.exit_codes = {
            Word(int('0000', 16)): 'No instructions left to execute.',
            Word(int('1000', 16)): 'Division by zero.',
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

            # --- Instruction execution ---
            self.execute_parsed_instruction(parsed_instruction)


    def execute_parsed_instruction(self, instruction: dict) -> None:
        # call instruction's corresponding function from dictionary
        self.INSTRUCTION_FUNCTIONS[instruction['instruction']](
            target = instruction['target'],
            op1 = instruction['first operand'],
            op2 = instruction['second operand'],
            immediate = instruction['immediate']
        )


    def _bitwise_and(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) & self.registers.read(op2)
        )
        self.program_counter.add(1)

    def _bitwise_or(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) | self.registers.read(op2)
        )
        self.program_counter += 1

    def _bitwise_xor(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) ^ self.registers.read(op2)
        )
        self.program_counter += 1

    def _bitwise_not(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            ~self.registers.read(op1)
        )
        self.program_counter += 1

    def _shift(self, target=None, op1=None, op2=None, immediate=None):
        to_shift = self.registers.read(op1)
        amount = self.registers.read(op2)
        if amount > 0:
            result = to_shift >> amount
        else:
            result = to_shift << -1*amount
        self.registers.write(target, result)
        self.program_counter += 1

    def _add(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) + self.registers.read(op2)
        )
        self.program_counter += 1

    def _sub(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) - self.registers.read(op2)
        )
        self.program_counter += 1

    def _mul(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) * self.registers.read(op2)
        )
        self.program_counter += 1

    def _int_div(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            target,
            self.registers.read(op1) // self.registers.read(op2)
        )
        self.program_counter += 1

    def _compare(self, target=None, op1=None, op2=None, immediate=None):
        a = self.registers.read(op1)
        b = self.registers.read(op2)
        if a > b:
            result = Word(int('10', 16))
        elif a < b:
            result = Word(int('1', 16))
        else:
            result = Word(int(0))
        self.registers.write(target, result)
        self.program_counter += 1

    def _load_immediate(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(target, immediate)
        self.program_counter += 1

    def _add_to_memory_counter(
    self, target=None, op1=None, op2=None, immediate=None):
        self.memory_counter += self.registers.read(op1) + immediate
        self.program_counter += 1

    def _load_word(self, target=None, op1=None, op2=None, immediate=None):
        self.registers.write(
            self.memory.load_word(self.memory_counter)
        )
        self.program_counter += 1

    def _store_word(self, target=None, op1=None, op2=None, immediate=None):
        self.memory.store_word(
            self.memory_counter,
            self.registers.read(op1)
        )
        self.program_counter += 1

    def _custom_register_immediate_input_output(
    self, target=None, op1=None, op2=None, immediate=None):
        # placeholder implementation
        if immediate == Word(0):
            print(self.registers.read(op1))
        elif immediate == Word(1):
            self.registers.write(op1, input())
        self.program_counter += 1

    def _add_to_program_counter_if_X_is_equal_to_zero(
    self, target=None, op1=None, op2=None, immediate=None):
        if self.registers.read('X') == Word(0):
            self.program_counter += immediate


if __name__=='__main__':
    cpu = CPU(64)
    cpu.load_memory_from('bytes_test')
    #cpu.memory.store_word(0, int('1000', 16))
    cpu.execute()
    print(cpu.memory)
