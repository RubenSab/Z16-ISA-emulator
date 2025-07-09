from word import Word
class PeripheralsInterfaceUnit:
    def __init__(self, cpu):
        self.cpu = cpu
        self.commands = {
            Word(1): self._print_base_10,
            Word(2): self._print_base_16,
            Word(3): self._print_ascii,
            Word(-1): self._input_base_10,
            Word(-2): self._input_base_16,
            Word(-3): self._input_ascii,
        }

    def execute_command(self, code: Word, register_name: str):
        self.commands[code](register_name)

    def _print_base_10(self, register_name):
        print(self.cpu.registers.read(register_name).str_by_base(10))

    def _print_base_16(self, register_name):
        print(self.cpu.registers.read(register_name).str_by_base(16))

    def _print_ascii(self, register_name):
        print(chr(self.cpu.registers.read(register_name)))

    def _input_base_10(self, register_name):
        self.cpu.registers.write(register_name, Word(int(input('> '))))

    def _input_base_16(self, register_name):
        self.cpu.registers.write(register_name, Word(int(input('> '), 16)))

    def _input_ascii(self, register_name):
        self.cpu.registers.write(register_name, Word(ord(input('> '))))
