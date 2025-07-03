from assembler import Assembler
from memory import Memory
from registers import Registers
from deassembler import Deassembler

if __name__=='__main__':
    assembler = Assembler()
    assembler.assemble('test')
    assembler.store_bytes('bytes_test')
    m = Memory(64)
    m.load_file('bytes_test')
    d = Deassembler()
    print(d.deassemble('bytes_test'))

