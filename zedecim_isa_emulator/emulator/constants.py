REGISTER_NAMES = list("OABCDEFGHIJKLMNX")

INSTRUCTIONS = {
    "and": 'R',
    "or": 'R',
    "xor": 'R',
    "not": 'R',
    "sh": 'R',
    "add": 'R',
    "sub": 'R',
    "mul": 'R',
    "div": 'R',
    "comp": 'R',
    "li": "RI",
    "amc": "RI",
    "lwmc": "RI",
    "swmc": "RI",
    "piu": "RI",
    "apceq": "RI",
}

INSTRUCTIONS_LIST = list(INSTRUCTIONS.keys())