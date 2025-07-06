from emulator import Emulator

if __name__=='__main__':

    emulator = Emulator(128)
    emulator.execute_code('example/zero.zed')
