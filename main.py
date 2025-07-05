from emulator import Emulator

if __name__=='__main__':

    emulator = Emulator(128)
    emulator.emulate_code('example/test.zed', 'example/memory.bin')
    #emulator.emulate_bin('example/memory.bin')
