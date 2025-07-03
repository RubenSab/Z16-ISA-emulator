from word import Word
from instructions import INSTRUCTIONS, INSTRUCTIONS_LIST
from registers import REGISTER_NAMES

class Deassembler:
    def __init__(self):
        pass


    def deassemble(self, filename) -> list:
        with open(filename, "rb") as f:
            byte_sequence = f.read()

        word_strings = [
            self._deassemble_word(
                str(Word.from_bytes(byte_sequence[i:i+2]).to_hex())
            )
            for i in range(0, len(byte_sequence), 2)
        ]

        return word_strings


    def _deassemble_word(self, word: str) -> dict:
        instruction = INSTRUCTIONS_LIST[int(word[0], 16)]
        if INSTRUCTIONS[instruction] == 'R':
            return {
                "instruction": instruction,
                "target": REGISTER_NAMES[int(word[1], 16)],
                "first operand": REGISTER_NAMES[int(word[2], 16)],
                "second operand": REGISTER_NAMES[int(word[3], 16)]
            }
        elif INSTRUCTIONS[instruction] == 'RI':
            return {
                "instruction": instruction,
                "target": REGISTER_NAMES[int(word[1], 16)],
                "first operand": int(Word(int(word[2:], 16), bit_width=8))
            }
        elif INSTRUCTIONS[instruction] == 'I':
            print('true')
            return {
                "instruction": instruction,
                "first operand": int(Word(int(word[2:], 16), bit_width=12))
            }


