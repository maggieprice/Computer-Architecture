"""CPU functionality."""

import sys

HLT = 0b00000001 
LDI = 0b10000010 
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101 
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ir = {
        LDI: self.LDI,
        PRN: self.PRN,
        HLT: self.HLT,
        MUL: self.MUL,
        POP: self.POP,
        PUSH: self.PUSH,
        CALL: self.CALL,
        RET: self.RET,
        CMP = self.CMP
        JMP = self.JMP
        JEQ = self.JEQ
        JNE = self.JNE
        }
        self.memory = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.SP = 7
        self.FL = 1
        

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
        elif op =="CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.FL = 1
            else:
                self.FL = 0
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
        SP = self.SP
        self.reg[SP] = 0xf4
        while self.running:
            operand_a = self.ram_read(self.pc +1)
            operand_b = self.ram_read(self.pc +2)
            IR = self.ram_read(self.pc) #instruction register 
            if IR in self.ir:
                self.ir[IR](operand_a, operand_b)
            # elif IR == PUSH:
                
    def ram_write(self, MDR, MAR):
        self.memory[MAR] = [MDR]
    
    def ram_read(self, MAR):
        MDR = self.memory[MAR]
        return MDR

    def equal(self, FL):
        #`E` Equal: during a `CMP`, set to 1 if registerA is equal to registerB, zero otherwise.
        # while CMP:
        FL = self.memory[FL]
        #     if registerA == registerB:
        #         E = 1
        #         return E
        #     else:
        #         E = 0
        #         return E
    
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


    def POP(self, operand_a, operand_b):
        # Pop the value at the top of the stack into the given register.
        # Copy the value from the address pointed to by SP to the given register.
        # Increment SP.
        SP = self.SP
        reg_num = self.memory[self.pc + 1]
        self.reg[reg_num] = self.memory[self.reg[SP]]
        self.reg[SP] += 1
        self.pc += 2


    def PUSH(self, operand_a, operand_b):
        # Push the value in the given register on the stack.
        # Decrement the SP.
        # Copy the value in the given register to the address pointed to by SP.
        SP = self.SP
        self.reg[SP] -= 1
        # Get the value we want to store from the register
        reg_num = self.memory[self.pc + 1]
        val = self.reg[reg_num]  # <-- this is the value that we want to push
        # Figure out where to store it
        top_of_stack_addr = self.reg[SP]
        # Store it
        self.memory[top_of_stack_addr] = val
        self.pc += 2
    
    def CALL(self, operand_a, operand_b):
        # 1. The address of the ***instruction*** _directly after_ `CALL` is
        # pushed onto the stack. This allows us to return to where we left off when the subroutine finishes executing.
        # 2. The PC is set to the address stored in the given register. We jump to that location in RAM and execute the first instruction in the subroutine. The PC can move forward or backwards from its current location.
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        SP = self.SP
        # Where we're going to RET to
        return_addr = self.pc + 2  
        # Push on the stack
        self.reg[SP] -= 1
        self.memory[self.reg[SP]] = return_addr
        # Get the address to call
        reg_num = self.memory[self.pc + 1]
        subroutine_addr = self.reg[reg_num]
        # Call it
        self.pc = subroutine_addr


    def RET(self, operand_a, operand_b):
        # Return from subroutine.
        # Pop the value from the top of the stack and store it in the `PC`.
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        SP = self.SP
        # return_addr = self.pc + 2
        
        # reg_num = self.memory[self.pc + 2]
        # subroutine_addr = self.reg[reg_num]
        # Call it
        self.pc = self.memory[self.reg[SP]]
        self.reg[SP] += 1

    def CMP(self):
        # Compare the values in two registers.
        # * If they are equal, set the Equal `E` flag to 1, otherwise set it to 0.
            FL = self.memory[FL]
            E = self.memory[E]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            self.alu("CMP", operand_a, operand_b)
            self.pc += 3
        
    

    def JMP(self):
        # Jump to the address stored in the given register.
        # Set the `PC` to the address stored in the given register.
        reg_num = self.memory[self.pc + 1]
        self.pc = self.reg[reg_num]


    def JEQ(self, operand_a, operand_b):
        # If `equal` flag is set (true), jump to the address stored in the given register.
        


    def JNE(self, operand_a, operand_b):
        # If `E` flag is clear (false, 0), jump to the address stored in the given register.
        if self.FL is None:
            reg_num = self.memory[self.pc + 1]
            self.pc = self.reg[reg_num]


