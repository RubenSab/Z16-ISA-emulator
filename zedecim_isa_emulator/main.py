import argparse

from mercurial.thirdparty.zope.interface import named

from zedecim_isa_emulator.emulator.emulator import Emulator


def main():
    parser = argparse.ArgumentParser(
        prog="zedecim",
        description="Zedecim ISA Emulator: Run programs on the Zedecim virtual CPU."
    )

    parser.add_argument(
        "memory_byte_size", type=int,
        help="Amount of memory (in bytes) to allocate"
    )
    parser.add_argument(
        "code_filename",
        help="Path to the assembly code file (.zed) to execute"
    )
    parser.add_argument(
        "numbers_base", type=int, nargs="?",
        help="Optional number base for displaying CPU state (e.g., 2, 10, 16)"
    )
    parser.add_argument(
        "history_file", nargs="?",
        help="Optional path to save I/O history"
    )

    args = parser.parse_args()

    emulator = Emulator(args.memory_byte_size)
    emulator.execute_code(args.code_filename)

    if args.numbers_base:
        emulator.cpu.display_state(args.numbers_base)

    if args.history_file:
        emulator.cpu.piu.console.export_history(args.history_file)

    emulator.reset()

if __name__ == '__main__':
    main()