from assembler import Assembler
from memory import Memory
from deassembler import Deassembler

if __name__=='__main__':
    assembler = Assembler()
    assembler.assemble('test')
    assembler.store_bytes('bytes_test')
    m = Memory(64)
    m.load_file('bytes_test')
    m.store_word(5, 1)
    print(m)
    d = Deassembler()
    print(d.deassemble('bytes_test'))
