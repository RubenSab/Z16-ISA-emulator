from word import Word

REGISTER_NAMES = list("OABCDEFGHIJKLMNX")

class RegisterNameError(Exception):
    pass

class Registers:

    def __init__(self):
        self.registers = dict.fromkeys(REGISTER_NAMES, Word(0))

    def read(self, register_name):
        if register_name == 'O':
            return 0
        self.validate_register_name(register_name)        
        return self.registers[register_name]

    def write(self, register_name, content: Word):
        content = Word(content)
        if register_name == 'O':
            return
        self.validate_register_name(register_name)
        self.registers[register_name] = content

    def __repr__(self):
        return self.str_by_base(16)

    def str_by_base(self, base):
        if base not in (2, 10, 16):
            raise ValueError("Base must be 10 or 16")
        return '\n'.join(
            f"{reg}: {val.str_by_base(base)}"
            for reg, val in self.registers.items()
        )

    def validate_register_name(self, register_name):
        if register_name not in REGISTER_NAMES:
            raise RegisterNameError(
                f"register \"{register_name}\" doesn't exist"
            )
