"""CPU functionality."""

import sys

HLT = 0b00000001 
LDI = 0b10000010 
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ir = {
        LDI: self.LDI,
        PRN: self.PRN,
        HLT: self.HLT,
        MUL: self.MUL
        }
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False


    def load(self, filename):
        """Load a program into memory."""
        filename = sys.argv[1]
        
        address = 0
        with open(filename) as f:
            for line in f:
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.memory[address] = v
                address += 1
		
                


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
        self.running = True
        # while self.running:
        #     IR = self.memory[self.pc]
        #     self.ir[IR]()
        while self.running:
            opperand_a = self.ram_read(self.pc +1)
            opperand_b = self.ram_read(self.pc +2)
            IR = self.ram_read(self.pc) #instruction register 
            if IR in self.ir:
                self.ir[IR](opperand_a, opperand_b)
            # print("IR", IR)

    def ram_write(self, MDR, MAR):
        self.memory[MAR] = [MDR]
    
    def ram_read(self, MAR):
        MDR = self.memory[MAR]
        return MDR
    
    def HLT(self, operand_a, operand_b):
        self.running = False
        
    def LDI(self, operand_a, operand_b):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc +=3 


    def PRN(self, operand_a, operand_b):
        operand_a = self.ram_read(self.pc + 1)
        val = self.reg[operand_a]
        print(val)
        self.pc += 2

    def MUL(self, operand_a, operand_b):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3
        # Multiply the values in two regs together and store the result in regA.
