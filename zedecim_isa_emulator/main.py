import sys
from emulator.emulator import Emulator

def main():
    # Get execution settings
    memory_byte_size = int(sys.argv[1])
    code_filename = sys.argv[2]
    # Execute code
    emulator = Emulator(memory_byte_size)
    emulator.execute_code(code_filename)
    # Print CPU state
    numbers_base = int(sys.argv[3]) if len(sys.argv) > 3 else None
    if numbers_base:
        emulator.cpu.display_state(numbers_base)
    # Store input/output history
    history_file = sys.argv[4] if len(sys.argv) > 4 else None
    if history_file:
        emulator.cpu.piu.console.export_history(history_file)
    # Reset emulator
    emulator.reset()