from word import Word
from instructions import INSTRUCTIONS, INSTRUCTIONS_LIST
from registers import REGISTER_NAMES

#    def deassemble(self, filename) -> list:
#        with open(filename, "rb") as f:
#            byte_sequence = f.read()
#
#        word_strings = [
#            self._deassemble_word(
#                str(Word.from_bytes(byte_sequence[i:i+2]).to_hex())
#            )
#            for i in range(0, len(byte_sequence), 2)
#        ]

#        return word_strings

def deassemble_word(word: Word) -> dict:
    word = str(word)
    instruction = INSTRUCTIONS_LIST[int(word[0], 16)]
    instruction_type = INSTRUCTIONS[instruction]
    if instruction_type == 'R':
        return {
            "type": instruction_type,
            "instruction": instruction,
            "target": REGISTER_NAMES[int(word[1], 16)],
            "first operand": REGISTER_NAMES[int(word[2], 16)],
            "second operand": REGISTER_NAMES[int(word[3], 16)]
        }
    elif instruction_type == 'RI':
        return {
            "type": instruction_type,
            "instruction": instruction,
            "target": REGISTER_NAMES[int(word[1], 16)],
            "first operand": int(Word(int(word[2:], 16), bit_width=8))
        }
    elif instruction_type == 'I':
        return {
            "type": instruction_type,
            "instruction": instruction,
            "first operand": int(Word(int(word[2:], 16), bit_width=12))
        }
