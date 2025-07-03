from word import Word

REGISTER_NAMES = list("OABCDEFGHIJKLMNX")

class RegisterNameError(Exception):
    pass

class Registers:

    def __init__(self):
        self.registers = dict.fromkeys(REGISTER_NAMES, 0)

    def read_word(self, register_name):
        if register_name == 'O':
            return 0
        self.validate_register_name(register_name)        
        return self.registers[register_name]

    def write_word(self, register_name, content: Word):
        content = Word(content)
        if register_name == 'O':
            pass
        self.validate_register_name(register_name)
        self.registers[register_name] = content

    def __repr__(self):
        return '\n'.join(
            f"{reg}: {val}" for reg, val in self.registers.items()
        )

    def validate_register_name(self, register_name):
        if register_name not in REGISTER_NAMES:
            raise RegisterNameError(
                f"register \"{register_name}\" doesn't exist"
            )
