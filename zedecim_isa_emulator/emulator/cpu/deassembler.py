from emulator.word import Word
from emulator.constants import INSTRUCTIONS, INSTRUCTIONS_LIST, REGISTER_NAMES


def deassemble_word(word: Word) -> dict:
    word = str(word)
    instruction = INSTRUCTIONS_LIST[int(word[0], 16)]
    instruction_type = INSTRUCTIONS[instruction]
    if instruction_type == 'R':
        return {
            "instruction": instruction,
            "first register": REGISTER_NAMES[int(word[1], 16)],
            "second register": REGISTER_NAMES[int(word[2], 16)],
            "third register": REGISTER_NAMES[int(word[3], 16)],
            "immediate": None
        }
    elif instruction_type == 'RI':
        return {
            "instruction": instruction,
            "first register": None,
            "second register": REGISTER_NAMES[int(word[1], 16)],
            "third register": None,
            "immediate": int(Word(int(word[2:], 16), bit_width=8))
        }
