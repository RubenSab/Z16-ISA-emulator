from assembler import Assembler
from cpu import CPU

if __name__=='__main__':

    # Assemble code
    assembler = Assembler()
    assembler.assemble('test.z')
    assembler.store_bytes('bytes.bin')

    # Execute
    cpu = CPU(512)
    cpu.load_memory_from('bytes.bin')
    cpu.execute()
    print(cpu.registers)
    print(cpu.memory)
    print(cpu.memory.program_counter)
    print(cpu.memory.memory_counter)
    print(cpu.exit_code)
