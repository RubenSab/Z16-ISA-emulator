from emulator.word import Word
from functools import wraps
from emulator.devices.console import Console

class PeripheralsInterfaceUnit:
    def __init__(self, cpu):
        self.cpu = cpu
        self.commands = {
            # Outputs
            Word(1): self._print_base_10,
            Word(2): self._print_base_2,
            Word(3): self._print_ascii,
            Word(4): self._print_base_16,
            # Inputs
            Word(-1): self._input_base_10,
            Word(-2): self._input_base_2,
            Word(-3): self._input_ascii,
            Word(-4): self._input_base_16,
        }
        self.console = Console()

    def execute_command(self, code: Word, register_name: str):
        self.commands[code](register_name)

    def _print_base_10(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).str_by_base(10)
        )
    def _print_base_2(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).str_by_base(2)
        )

    def _print_ascii(self, register_name):
        self.console.output(
            chr(self.cpu.registers.read(register_name))
        )

    def _print_base_16(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).str_by_base(16)
        )

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
        data = self.console.get_input()
        self.cpu.registers.write(register_name, Word(int(data)))

    @input_exception
    def _input_base_2(self, register_name):
        data = self.console.get_input()
        self.cpu.registers.write(register_name, Word(int(data, 2)))

    @input_exception
    def _input_ascii(self, register_name):
        data = self.console.get_input()
        self.cpu.registers.write(register_name, Word(ord(data)))

    @input_exception
    def _input_base_16(self, register_name):
        data = self.console.get_input()
        self.cpu.registers.write(register_name, Word(int(data, 16)))