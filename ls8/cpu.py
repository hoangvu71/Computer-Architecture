"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
    def load(self, argv):
        """Load a program into memory."""


        def load_read_file(argv, ram):
            address = 0

            try:
                with open(argv) as f:
                    for line in f:
                        line = line.strip()
                        line1 = line.split()
                        print(line1)

                        if len(line1) == 0:
                            continue
                        
                        if line1[0][0] == '#':
                            continue
                        
                        try:
                            self.ram[address] = int(line1[0], 2)
                            address += 1
                        except ValueError:
                            print(f"Invalid number: {line1[0]}")
                            sys.exit(1)
            except FileNotFoundError:
                print(f"Couldn't open file")
                sys.exit(2)
            

            print(ram)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        load_read_file(argv, self.ram)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010

        instructions_dict = {}
        instructions_dict[LDI] = self.LDI
        instructions_dict[MUL] = self.MUL
        instructions_dict[PRN] = self.PRN

        running = True
        while running:
            ir = self.ram[self.pc]
            operand_a = self.ram[self.pc + 1]
            operand_b = self.ram[self.pc + 2]
            if ir == LDI:
                instructions_dict[LDI](operand_a, operand_b)

            elif ir == PRN:
                instructions_dict[PRN](operand_a)

            elif ir == MUL:
                instructions_dict[MUL](operand_a, operand_b)

            elif ir == HLT:
                running = False
                
            else:
                print("something is wrong")
                sys.exit(3)

    def LDI(self, operand_a, operand_b):
        self.ram_write(operand_a, operand_b)
        self.pc += 3

    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
    
    def PRN(self, operand_a):
        print(self.ram_read(operand_a))
        self.pc += 2

    def ram_read(self, index):
        value = self.reg[index]
        return value

    def ram_write(self, index, value):
        self.reg[index] = value
