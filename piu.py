from word import Word
from functools import wraps

class PeripheralsInterfaceUnit:
    def __init__(self, cpu):
        self.cpu = cpu
        self.commands = {
            Word(1): self._print_base_10,
            Word(2): self._print_base_2,
            Word(3): self._print_ascii,
            Word(4): self._print_base_16,
            Word(-1): self._input_base_10,
            Word(-2): self._input_base_2,
            Word(-3): self._input_ascii,
            Word(-4): self._input_base_16,
        }

    def execute_command(self, code: Word, register_name: str):
        self.commands[code](register_name)

    def _print_base_10(self, register_name):
        print(self.cpu.registers.read(register_name).str_by_base(10))

    def _print_base_2(self, register_name):
        print(self.cpu.registers.read(register_name).str_by_base(2))

    def _print_ascii(self, register_name):
        print(chr(self.cpu.registers.read(register_name)))

    def _print_base_16(self, register_name):
        print(self.cpu.registers.read(register_name).str_by_base(16))

    def input_exception(func):
        @wraps(func)
        def wrapper(self, register_name):
            try:
                return func(self, register_name)
            except ValueError as e:
                print(
                    f"\nInput Error: {e}.\n"
                    f"Ignoring input and setting register {register_name} to 0."
                )
                self.cpu.registers.write(register_name, Word(0))
                return None

        return wrapper

        return wrapper

    @input_exception
    def _input_base_10(self, register_name):
        self.cpu.registers.write(register_name, Word(int(input('> '))))

    @input_exception
    def _input_base_2(self, register_name):
        self.cpu.registers.write(register_name, Word(int(input('> '), 2)))

    @input_exception
    def _input_ascii(self, register_name):
        self.cpu.registers.write(register_name, Word(ord(input('> '))))

    @input_exception
    def _input_base_16(self, register_name):
        self.cpu.registers.write(register_name, Word(int(input('> '), 16)))