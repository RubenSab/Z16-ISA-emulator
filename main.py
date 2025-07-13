from emulator.emulator import Emulator

if __name__=='__main__':

    emulator = Emulator(
        memory_byte_size = 64,
        print_base = 16 # used for printing the CPU state at the end
    )
    emulator.execute_code('examples/zero.zed')
