# Zedecim ISA

Zedecim is an Instruction Set (emulated) Architecture which has sixteen instructions (Sedecim in latin) and it can only work with signed 16 bit integers (Z in the name stands for the set of integer numbers).

# Usage

Launch `main.py` from the command line or do the following:

1. Import `emulator` (emulator.py) from `Emulator`.
2. Initialize the emulator with the desired memory size in bytes.
3. Then you can either **run Zedecim assembly code**, optionally specifying a file where to export the memory in a binary file, or **run from a binary file**.

``` python
from emulator import Emulator

emulator = Emulator(128)
emulator.emulate_code('example/test.zed', 'example/memory.bin')
# Or if you already have the binary file ready:
# emulator.emulate_bin('example/test.bin')
```

# Emulator structure

**emulator.py** which launches the emulation is made from **multiple modules**:
- **assembler.py** that translates assembly language to binary data;
- **deassembler.py** that decodes binary data into instructions
- **cpu.py** that executes the binary data, made from this modules:
	- **memory.py**, populated both by instructions and data produced by code, stored as words using **word.py**;
	- **registers.py**;
	- **counter.py**, used in moth Memory Counter and Program Counter;
	- **instructions.py**, which contains instruction's names along their type.

# Zedecim Architecture
## Memory elements

Zedecim has:

- 16 general purpose **Registers** named O, A, B, C, D, E, F, G, H, I, J, K, L, M, N, X. The register **O** is **hard coded to 0**, while the register **X** is used for **branching conditions**;
- A custom sized **Memory** addressed by **16 bits long words**. Conventionally, the first half is used for instructions, while the second one is used as data memory;
- A **Program Counter** to fetch the current instruction, sized accordingly to the memory in order to address the whole memory space;
- A **Memory Counter** used in store/load to memory instructions, sized accordingly to the memory in order to address the whole memory space. It's introduced because 16 bit registers can't address a memory space of arbitrary length;

## Instructions

### Formats

Instructions have only 3 possible formats, in which fields are evenly divided in nibbles (4 bits). The same order and type of operands holds for **Zedecim's Assembly**:
- **R** (Register type):
	- 1 nibble for the instruction code,
	- 1 nibble for the target register,
	- 1 nibble for the first operand's register,
	- 1 nibble for the second operand's register
- **RI** (Register immediate type):
	- 1 nibble for the instruction code,
	- 1 nibble for the first register (either target or first operand's),
	- 2 nibbles for the signed immediate field (-128 to 127)
- **I** (Immediate type):
	- 1 nibble for the instruction code,
	- 3 nibbles for the signed immediate field (-2048 to 2047) 

### Instruction list

*Labelled by their code, registers are named r1, r2, r3*
#### R type

0. `and` (bitwise and)
1. `or` (bitwise or)
2. `xor` (bitwise xor)
3. `not` (bitwise not, r2 is ignored)
4. `sh` (shift r2 to the right with positive values of r3 and to the left with negative values)
5. `add` (addition)
6. `sub` (subtraction)
7. `mul` (multiplication)
8. `div` (integer division)
9. `comp`, sets r1 to:
	- `10` if r2>r3,
	- `1` if r2<r3,
	- `0` if r2=r3.

#### RI type

10. `li` (load immediate to r1)
11. `amc` (add r1 + immediate field to memory counter)
12. `lwmc` (load word to r1 from address = memory counter + immediate)
13. `swmc` (store word in r1 to address = memory counter + immediate)
14. `criio` (*Custom Register Immediate Input Output*: inputs to or outputs the content of r1 according to the mode expressed in the immediate field. Its behaviour depends on the custom architecture implementation.)

#### I type

15. apceq (add the immediate offset to program counter if the register **X** is equal to 0)

# Zedecim Assembly syntax

Syntax follows these core rules:

- Instruction's name and operands are written **in the same order** as they are formatted according to the instruction type, separated by a space.
- Instruction names are written in *lowercase*.
- Register names are written in *uppercase*.
- No immediate or register is implicit.
- There can be empty lines.
- Comments can be written starting with an `#` both after instructions and in empty lines.

Also, the following conventions are encouraged:

- If the instruction immediate field **is greater or equal to zero** and **is added to a counter** (`amc`, `lwmc`, `swmc`, `apceq`), then it's prefixed by a **plus sign**.
- In every other case, operands should be separated by a comma and a space.
- Assembly files are in `.zed` format.

Example of semantically correct instructions:

```
# R type
add C, A, B

# RI type
li D, 8
swmc D, +0

# I type
apceq -2571
```
