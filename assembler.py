from word import Word
from registers import REGISTER_NAMES
from instructions import INSTRUCTIONS, INSTRUCTIONS_LIST

class InvalidInstruction(Exception):
    pass

class InvalidOperands(Exception):
    pass


class Assembler:

    def __init__(self):
        self.byte_code = None

    def assemble(self, filename) -> bytes:
        with open(filename, 'r') as f:
            parsed_lines = [
                line.split('#')[0].strip()
                .replace(',',' ').replace('+',' ').split()
                for line in f.readlines()
                if line.split('#')[0].strip().split()
            ]

        words = []
        for line in parsed_lines:

            instruction, operands = line[0], line[1:]
            instruction_type = INSTRUCTIONS[instruction]
            hex_string = self._translate_instruction(instruction) + \
            self._translate_operands(operands, instruction_type)

            words.append(bytes.fromhex(hex_string))

        byte_code = b''.join(words)
        self.byte_code = byte_code
        return byte_code


    def _translate_instruction(self, name):
        if name not in INSTRUCTIONS_LIST:
            raise InvalidInstruction(f"Instruction {name} doesn't exist")
        return self._hex_index(INSTRUCTIONS_LIST, name)


    def _translate_operands(self, operands, instruction_type):
        if instruction_type == 'R':
            if len(operands) != 3 or \
            operands[0] not in REGISTER_NAMES or \
            operands[1] not in REGISTER_NAMES or \
            operands[2] not in REGISTER_NAMES:
                raise InvalidOperands(
                    f"Invalid operands {operands} for instruction type R."
                )
            return self._hex_index(REGISTER_NAMES, operands[0]) + \
            self._hex_index(REGISTER_NAMES, operands[1]) + \
            self._hex_index(REGISTER_NAMES, operands[2])

        elif instruction_type == 'RI':
            if len(operands) != 2 or \
            operands[0] not in REGISTER_NAMES or \
            operands[1] in REGISTER_NAMES:
                raise InvalidOperands(
                    f"Invalid operands {operands} for instruction type RI."
                )
            return self._hex_index(REGISTER_NAMES, operands[0]) + \
            str(Word(int(operands[1]), 8))

        elif instruction_type == 'I':
            if len(operands) != 1 or operands[0] in REGISTER_NAMES:
                raise InvalidOperands(
                    f"Invalid operands {operands} for instruction type I."
                )
            return str(Word(int(operands[0]), 12))


    def _hex_index(self, List, element):
        return str(hex(List.index(element)))[2:]


    def store_bytes(self, filename):
        with open(filename, 'wb') as f:
            f.write(self.byte_code)
