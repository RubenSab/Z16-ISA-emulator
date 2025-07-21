
Zedecim is an Instruction Set (emulated) Architecture which has sixteen instructions (Sedecim in latin) and it can only work with signed 16 bit integers (Z in the name stands for the set of integer numbers).

# Emulator installation (CLI)

1. run `git clone https://github.com/RubenSab/Zedecim-ISA-emulator`
2. move into the cloned repo: `cd Zedecim-ISA-emulator`
3. run `pip install .`

# Usage

## As a CLI program
Run `zedecim <memory_byte_size> <code_filename> [print_base] [history_file]`

Arguments:
- memory_byte_size: Amount of memory (in bytes) to allocate
- code_filename: Path to the assembly code file to execute
- numbers_base: Optional number base for displaying CPU state (e.g., 2, 10, 16)
- history_file: Optional path to save I/O history

## As a python class

Move `emulator` directory into your current project directory, then you can
interact with the emulator using its methods.

For more information, read emulator.py methods docstrings.

``` python
from emulator.emulator import Emulator

emulator = Emulator(memory_byte_size = 64)
emulator.execute_code('example/zero.zed')
emulator.cpu.display_state(base = 16)

# Or if you already have the binary file ready:
# emulator.execute_bin('example/test.bin')
# emulator.cpu.display_state(base = 16)
```

# Emulator structure

**emulator.py** which launches the emulation is made from **multiple modules**:
- **assembler.py** that translates assembly language to binary data;
- **deassembler.py** that decodes binary data into instructions
- **cpu.py** that executes the binary data, made from this modules:
    - **registers.py**;
    - **memory.py**, populated both by instructions and data produced by code, stored as words using **word.py**;
    - **piu**: Peripherals Interface Unit, used to input/output registers content;
    - **counter.py**, used for both Memory Counter and Program Counter;
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

Instructions have only 2 possible formats, in which fields are evenly divided in nibbles (4 bits). The same order and type of operands holds for **Zedecim's Assembly**:
- **R** (Register type):
	- 1 nibble for the instruction code,
	- 1 nibble for the target register,
	- 1 nibble for the first operand's register,
	- 1 nibble for the second operand's register
- **RI** (Register immediate type):
	- 1 nibble for the instruction code,
	- 1 nibble for the first register (either target or first operand's register),
	- 2 nibbles for the signed immediate field [-128 to 127]

### Instruction list

*Labelled by their code, registers are named r1, r2, r3*
#### R type: *two registers* as *input* and output in a register

0. `and` (bitwise and)
1. `or` (bitwise or)
2. `xor` (bitwise xor)
3. `not` (bitwise not, r2 is ignored)
4. `sh` (shift r2 to the right with positive values of r3 and to the left with negative values)
5. `add` (addition)
6. `sub` (subtraction)
7. `mul` (multiplication)
8. `div` (division)
9. `comp`, sets r1 to:
	- `1` if r2>r3,
	- `-1` if r2<r3,
	- `0` if r2=r3.

#### RI type: a *register* and an *immediate* as *input* and output either in a register, a memory location, the memory counter, the program counter or a peripheral

10. `li` (loads immediate to register)
11. `amc` (adds register + immediate to memory counter)
12. `lwmc` (loads word to register from address = memory counter + immediate)
13. `swmc` (stores word in register to address = memory counter + immediate)
14. `piu` (*Peripherals Interface Unit*: inputs to or outputs the register content using the device/mode expressed in the immediate field. Its behaviour can depend on the custom architecture implementation.)
15. `apceq` (adds register + immediate to program counter if the register **X** is equal to 0)

### Special exit code instructions

Some **reserved R-type instructions**, otherwise useless, can trigger and **exit code** and halt the execution:

```
and O, O, O -> triggers exit code 0x0000: No instructions left to execute.
or O, O, O -> triggers exit code 0x1000: Division by zero.
xor O, O, O -> triggers exit code 0x2000: Custom I/O exit code 0x2000.
not O, O, O -> triggers exit code 0x3000: Custom I/O exit code 0x3000.
sh O, O, O -> triggers exit code 0x4000: Custom I/O exit code 0x4000.
add O, O, O -> triggers exit code 0x5000: Custom I/O exit code 0x5000.
sub O, O, O -> triggers exit code 0x6000: Custom I/O exit code 0x6000.
mul O, O, O -> triggers exit code 0x7000: Custom I/O exit code 0x7000.
div O, O, O -> triggers exit code 0x8000: Custom I/O exit code 0x8000.
comp O, O, O -> triggers exit code 0x9000: Custom I/O exit code 0x9000.
```
### `piu` immediate fields **as currently implemented in this emulator**

*Reminder: the immediate field of `piu` and other RI-type instructions can be a signed value in [-128, 127], so the Peripheral Interface Unit commands can only have codes in this range*.

#### Outputs
1. use Console device to print the register content as an ascii character.
2. use Console device to print the register content in base 2.
10. use Console device to print the register content in base 10.
16. use Console device to print the register content in base 16.
20. use Console device to print the register content in base 2, with ' ' as zeroes and '█' (U+2588) as ones. Useful to "draw" with numbers. 

#### Inputs (add minus before code)
1. use Console device to input an ascii character to the register.
2. use Console device to input a base 2 number to the register.
10. use Console device to input a base 10 number to the register.
16. use Console device to input a base 16 number to the register.

#### Overwrites
42. use RandomNumberGenerator to set the register to a random 16 bit (signed) number.

# Zedecim Assembly syntax

Syntax follows these core rules:

- Instruction's name and operands are written **in the same order** as they are formatted according to the instruction type, separated by a space.
- Instruction names are written in *lowercase*.
- Register names are written in *uppercase*.
- No immediate or register is implicit.
- There can be empty lines.
- Comments can be written starting with an `#` both after instructions and in empty lines.

Also, the following conventions are encouraged:

- If the immediate fields of `lwmc`, `swmc` are greater or equal to zero, they should prefixed by a **plus sign** to represent being offsets of the memory counter.
- Assembly files are in `.zed` format.

Example of semantically correct instructions:

```
# R type
add C, A, B

# RI type
li D, 8
swmc D, +0

# I type
apceq O, -25
```
