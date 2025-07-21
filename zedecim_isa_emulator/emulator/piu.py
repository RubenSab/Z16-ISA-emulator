from functools import wraps
from zedecim_isa_emulator.emulator.devices.random_number_generator import RandomNumberGenerator
from zedecim_isa_emulator.emulator.word import Word
from zedecim_isa_emulator.emulator.devices.console import Console

class PeripheralsInterfaceUnit:
    def __init__(self, cpu):
        self.cpu = cpu
        self.commands = {
            # Outputs
            Word(1): self._print_ascii,
            Word(2): self._print_base_2,
            Word(10): self._print_base_10,
            Word(16): self._print_base_16,
            Word(20): self._print_binary_blocks,
            # Inputs
            Word(-1): self._input_ascii,
            Word(-2): self._input_base_2,
            Word(-10): self._input_base_10,
            Word(-16): self._input_base_16,
            Word(-42): self._rng_out,
        }

        self.console = Console()
        self.rng = RandomNumberGenerator()

    def execute_command(self, code: Word, register_name: str):
        self.commands[code](register_name)

    def _print_base_10(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).str_by_base(10)
        )
    def _print_base_2(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).to_bin()
        )

    def _print_ascii(self, register_name):
        self.console.output(
            chr(self.cpu.registers.read(register_name))
        )

    def _print_base_16(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).to_hex()
        )

    def _print_binary_blocks(self, register_name):
        self.console.output(
            self.cpu.registers.read(register_name).to_bin()
            .replace('0', ' ').replace('1', '█')
        )
    # Input commands

    def input_exception(func):
        @wraps(func)
        def wrapper(self, register_name):
            try:
                return func(self, register_name)
            except ValueError as e:
                print(
                    f"\nInput Error: {e}.\n"
                    f"Ignoring input and setting register {register_name} to 0."
                    f"\n"
                )
                self.cpu.registers.write(register_name, Word(0))
                return None

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

    def _rng_out(self, register_name):
        data = self.rng.get_input()
        self.cpu.registers.write(register_name, Word(data))