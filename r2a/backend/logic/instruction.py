import utils

class Instruction:
    def __init__(self, raw_binary):
        self.raw_binary = raw_binary
        self.decoded = None

        self.opcode = None
        self.funct3 = None
        self.funct7 = None
        self.rd = None
        self.rs1 = None
        self.rs2 = None
        self.imm = None
        self.mnemonic = None

        self.immediate = None
        self.destination_register = None
        self.source_register_1 = None
        self.source_register_2 = None

    def __str__(self):
        return self.decode()
    
    def __int__(self):
        return self.raw_binary
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.raw_binary == other
        elif isinstance(other, Instruction):
            return self.raw_binary == other.raw_binary
        elif isinstance(other, str):
            return self.raw_binary == other.encode("utf-8")
        else:
            return False
    
    def decode(self):
        self.decoded = "unknown"
        return self.decoded

    @classmethod
    def from_binary(cls, raw_bytes):
        raw_binary = int.from_bytes(raw_bytes, "little")

        if len(raw_bytes) == 4:
            opcode = raw_binary & 0X7F

            if opcode in (0b11, 0b10011, 0b11011, 0b1100111, 0b1110011):
                return ITypeInstruction(raw_binary)
            elif opcode in (0X17, 0X37):
                return UTypeInstruction(raw_binary)
            elif opcode in (0b100011,):
                return STypeInstruction(raw_binary)
            elif opcode in (0b110011, 0b1110011):
                return RTypeInstruction(raw_binary)
            elif opcode in (0b1100011,):
                return BTypeInstruction(raw_binary)
            elif opcode in (0X6F,):
                return JTypeInstruction(raw_binary)
            
        elif len(raw_bytes) == 2:
            opcode = raw_binary & 0b11

            pass

        return Instruction(raw_binary)
    
    def get_opcode(self):
        return self.raw_binary & 0X7F
    
    def get_funct3(self):
        return (self.raw_binary >> 12) & 0b111
    
    def get_funct7(self):
        return (self.raw_binary >> 25)
    
    def get_rd(self):
        return (self.raw_binary >> 7) & 0b11111
    
    def get_rs1(self):
        return (self.raw_binary >> 15) & 0b11111
    
    def get_rs2(self):
        return (self.raw_binary >> 20) & 0b11111

class ITypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b11, 0b0): "lb",
            (0b11, 0b1): "lh",
            (0b11, 0b10): "lw",
            (0b11, 0b11): "ld",
            (0b11, 0b100): "lbu",
            (0b11, 0b101): "lhu",
            (0b11, 0b110): "lwu",
            (0b10011, 0b0): "addi",
            (0b10011, 0b1): "slli",
            (0b10011, 0b10): "slti",
            (0b10011, 0b11): "sltiu",
            (0b10011, 0b100): "xori",
            (0b10011, 0b101): "srli",
            (0b10011, 0b110): "ori",
            (0b10011, 0b111): "andi",
            (0b11011, 0b0): "addiw",
            (0b11011, 0b1): "slliw",
            (0b11011, 0b101): "srliw",
            (0b1100111, 0b0): "jalr",
            (0b1110011, 0b0): "ecall"
        }
        
        self.opcode = self.get_opcode()
        self.funct3 = self.get_funct3()
        self.rd = self.get_rd()
        self.rs1 = self.get_rs1()
        self.imm = (self.raw_binary >> 20) & 0b111111111111
        self.mnemonic = mnemonics[(self.opcode, self.funct3)]

        self.immediate = self.imm & 0b11111 if self.mnemonic in ("slli", "srli", "slliw", "srliw") else utils.twos_complement(self.imm)
        self.destination_register = utils.format_register(self.rd)
        self.source_register_1 = utils.format_register(self.rs1)

        self.mnemonic = "srai" if self.mnemonic == "srli" and self.get_funct7() == 0b0100000 else self.mnemonic
        self.mnemonic = "sraiw" if self.mnemonic == "srliw" and self.get_funct7() == 0b0100000 else self.mnemonic
        self.mnemonic = "unknown" if self.mnemonic == "ecall" and (self.rd != 0 or self.rs1 != 0) else self.mnemonic
        self.mnemonic = "ebreak" if self.mnemonic == "ecall" and self.imm == 0b1 else self.mnemonic

        if self.opcode == 0b11:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}({self.source_register_1})"
        elif self.opcode == 0b111011:
            self.decoded = self.mnemonic
        else:                                                                                                                                                                                   
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_1}, {self.immediate}"

        return self.decoded

class UTypeInstruction(Instruction):
    def decode(self):
         if self.decoded:
              return self.decoded
         
         self.opcode = self.get_opcode()
         self.mnemonic = "auipc" if self.opcode == 0b10111 else "lui"
         self.rd = self.get_rd()
         self.imm = (self.raw_binary >> 12)

         self.destination_register = utils.format_register(self.rd)
         self.immediate = self.imm

         self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}"

         return self.decoded

class STypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b100011, 0b11): "sd",
            (0b100011, 0b0): "sb",
            (0b100011, 0b1): "sh",
            (0b100011, 0b10): "sw"
        }
        
        self.opcode = self.get_opcode()
        self.funct3 = self.get_funct3()
        self.mnemonic = mnemonics[(self.opcode, self.funct3)]
        self.rs1 = self.get_rs1()
        self.rs2 = self.get_rs2()
        self.imm = ((self.raw_binary >> 20) & 0b111111100000) | ((self.raw_binary >> 7) & 0b11111)

        self.source_register_1 = utils.format_register(self.rs1)
        self.source_register_2 = utils.format_register(self.rs2)
        self.immediate = utils.twos_complement(self.imm)

        self.decoded = f"{self.mnemonic} {self.source_register_2}, {self.immediate}({self.source_register_1})"

        return self.decoded


class BTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1100011, 0b0): "beq",
            (0b1100011, 0b1): "bne",
            (0b1100011, 0b100): "blt",
            (0b1100011, 0b101): "bge",
            (0b1100011, 0b110): "bltu",
            (0b1100011, 0b111): "bgeu"
        }

        self.opcode = self.get_opcode()
        self.funct3 = self.get_funct3()
        self.mnemonic = mnemonics[(self.opcode, self.funct3)]
        self.rs1 = self.get_rs1()
        self.rs2 = self.get_rs2()
        self.imm = (((self.raw_binary >> 20) & 2048) | ((self.raw_binary << 4) & 0b10000000000) | ((self.raw_binary >> 21) & 0b1111110000) | ((self.raw_binary >> 8) & 0b1111)) << 1

        self.source_register_1 = utils.format_register(self.rs1)
        self.source_register_2 = utils.format_register(self.rs2)
        self.immediate = utils.twos_complement(self.imm)

        self.decoded = f"{self.mnemonic} {self.source_register_1}, {self.source_register_2}, {self.immediate}"

        return self.decoded


class RTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b110011, 0b0, 0b0): "add",
            (0b110011, 0b0, 0b1): "mul",
            (0b110011, 0b1, 0b1): "mulh",
            (0b110011, 0b10, 0b1): "mulsu",
            (0b110011, 0b11, 0b1): "mulu",
            (0b110011, 0b100, 0b1): "div",
            (0b110011, 0b101, 0b1): "divu",
            (0b110011, 0b110, 0b1): "rem",
            (0b110011, 0b111, 0b1): "remu",
            (0b110011, 0b0, 0b100000): "sub",
            (0b110011, 0b1, 0b0): "sll",
            (0b110011, 0b10, 0b0): "slt",
            (0b110011, 0b11, 0b0): "sltu",
            (0b110011, 0b100, 0b0): "xor",
            (0b110011, 0b101, 0b0): "srl",
            (0b110011, 0b101, 0b100000): "sra",
            (0b110011, 0b110, 0b0): "or",
            (0b110011, 0b111, 0b0): "and",
            (0b111011, 0b0, 0b0): "addw",
            (0b111011, 0b0, 0b100000): "subw",
            (0b111011, 0b1, 0b0): "sllw",
            (0b111011, 0b101, 0b0): "srlw",
            (0b111011, 0b101, 0b100000): "sraw"
        }

        self.opcode = self.get_opcode()
        self.funct3 = self.get_funct3()
        self.funct7 = self.get_funct7()
        self.mnemonic = mnemonics[(self.opcode, self.funct3, self.funct7)]
        self.rd = self.get_rd()
        self.rs1 = self.get_rs1()
        self.rs2 = self.get_rs2()

        self.destination_register = utils.format_register(self.rd)
        self.source_register_1 = utils.format_register(self.rs1)
        self.source_register_2 = utils.format_register(self.rs2)

        self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_1}, {self.source_register_2}"

        return self.decoded

class JTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        self.opcode = self.get_opcode()
        self.mnemonic = "jal"
        self.rd = self.get_rd()
        self.imm = (((self.raw_binary >> 12) & 524288) | ((self.raw_binary >> 1) & 0b1111111100000000000) | ((self.raw_binary >> 9) & 0b10000000000) | ((self.raw_binary >> 21) & 0b1111111111)) << 1

        self.destination_register = utils.format_register(self.rd)
        self.immediate = utils.twos_complement(self.imm)

        self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}"

        return self.decoded