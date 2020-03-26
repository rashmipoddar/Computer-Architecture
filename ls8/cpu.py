"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    """ 
    1 byte = 8 bits  
    Each bit can contain either 0 or 1 so we have 2 possibilities for each bit 
    and 2^8 = 256 possibilities for 8 bits and the numbers are from 0 to 255 .
    """

    def __init__(self):
        """Construct a new CPU."""
        self.register = [0] * 8
        self.pc = 0 # Program counter i.e. the current instruction
        self.ram = [0] * 256
        self.stack_pointer = self.register[7]
        self.register[7] = 0xF4

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1
            # print(self.ram)

    def load_dynamic(self, filename):
        address = 0
        # print('Filename passed to the load function: ', filename)
        try:
            with open(filename) as f:
                # The filename takes the path of the file to open like examples/print8.ls8
                for line in f:
                    # Ignore comments
                    comment_split = line.split("#")
                    # Strip out whitespace
                    num = comment_split[0].strip()
                    # Ignore blank lines
                    if num == '':
                        continue    
                    value = int(num, 2)
                    self.ram_write(address, value)
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)
        # print(self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        elif op == "MUL":
            self.register[reg_a] = self.register[reg_a] * self.register[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def run(self):
        """Run the CPU."""
        # print('Register: ', self.register)
        running = True
        
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
            
        while running:
            command = self.ram[self.pc]
            if command == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.register[operand_a] = operand_b
                self.pc += 3

            elif command == PRN:
                operand_a = self.ram_read(self.pc + 1)
                print(self.register[operand_a])
                self.pc += 2

            elif command == HLT:
                running = False
                self.pc += 1

            elif command == MUL:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                self.alu('MUL', operand_a, operand_b)
                self.pc += 3

            elif command == PUSH:
                # Push the value in the given register on the stack.
                operand_a = self.ram_read(self.pc + 1)
                value = self.register[operand_a]
                # 1. Decrement the `SP`.
                self.stack_pointer -= 1
                # 2. Copy the value in the given register to the address pointed to by `SP`.
                self.ram[self.stack_pointer] = value
                self.pc += 2

            elif command == POP:
                # Pop the value at the top of the stack into the given register.
                operand_a = self.ram_read(self.pc + 1)
                # 1. Copy the value from the address pointed to by `SP` to the given register.
                self.register[operand_a] = self.ram[self.stack_pointer]
                # 2. Increment `SP`.
                self.stack_pointer += 1
                self.pc += 2

            else:
                print(f"Unknown instruction: {command}")
                sys.exit(1)
