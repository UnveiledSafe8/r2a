import utils
import decode

class Instruction:
    def __init__(self, raw_binary):
        self.raw_binary = raw_binary
        self.bitfields = decode.BitFieldDecoder(raw_binary)
        self.decoded = None

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
            opcodeRegistry = {
                0b11: ITypeInstruction,
                0b10011: ITypeInstruction,
                0b11011: ITypeInstruction,
                0b1100111: ITypeInstruction,
                0b1110011: ITypeInstruction,
                0b10111: UTypeInstruction,
                0b110111: UTypeInstruction,
                0b100011: STypeInstruction,
                0b110011: RTypeInstruction,
                0b111011: RTypeInstruction,
                0b101111: RTypeInstruction,
                0b1100011: BTypeInstruction,
                0b1101111: JTypeInstruction,
                0b1111: MiscTypeInstruction
            }

            opcode = raw_binary & 0X7F

            if opcode in opcodeRegistry:
                return opcodeRegistry[opcode](raw_binary)
            else:
                return Instruction(raw_binary)
            
        elif len(raw_bytes) == 2:
            opcode = raw_binary & 0b11

        return Instruction(raw_binary)

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
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        self.immediate = self.bitfields.i_imm & 0b11111 if self.mnemonic in ("slli", "srli", "slliw", "srliw") else utils.twos_complement(self.bitfields.i_imm, 12)
        self.destination_register = utils.format_register(self.bitfields.rd)
        self.source_register_1 = utils.format_register(self.bitfields.rs1)

        self.mnemonic = "srai" if self.mnemonic == "srli" and self.bitfields.funct7 == 0b0100000 else self.mnemonic
        self.mnemonic = "sraiw" if self.mnemonic == "srliw" and self.bitfields.funct7 == 0b0100000 else self.mnemonic
        self.mnemonic = "unknown" if self.mnemonic == "ecall" and (self.bitfields.rd != 0 or self.bitfields.rs1 != 0) else self.mnemonic
        self.mnemonic = "ebreak" if self.mnemonic == "ecall" and self.bitfields.i_imm == 0b1 else self.mnemonic

        if self.bitfields.opcode == 0b11:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}({self.source_register_1})"
        elif self.bitfields.opcode == 0b111011:
            self.decoded = self.mnemonic
        else:                                                                                                                                                                                   
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_1}, {self.immediate}"
        return self.decoded

class UTypeInstruction(Instruction):
    def decode(self):
         if self.decoded:
              return self.decoded
         
         mnemonics = {
            (0b10111,): "auipc",
            (0b110111,): "lui"
        }
         
         self.mnemonic = mnemonics.get((self.bitfields.opcode,), "unknown")
         self.destination_register = utils.format_register(self.bitfields.rd)
         self.immediate = self.bitfields.u_imm

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
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        self.source_register_1 = utils.format_register(self.bitfields.rs1)
        self.source_register_2 = utils.format_register(self.bitfields.rs2)
        self.immediate = utils.twos_complement(self.bitfields.s_imm, 12)

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

        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        self.source_register_1 = utils.format_register(self.bitfields.rs1)
        self.source_register_2 = utils.format_register(self.bitfields.rs2)
        self.immediate = utils.twos_complement(self.bitfields.b_imm, 13)

        self.decoded = f"{self.mnemonic} {self.source_register_1}, {self.source_register_2}, {self.immediate}"
        return self.decoded


class RTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b101111, 0b10, 0b10): "lr.w",
            (0b101111, 0b10, 0b11): "sc.w",
            (0b101111, 0b10, 0b1): "amoswap.w",
            (0b101111, 0b10, 0b0): "amoadd.w",
            (0b101111, 0b10, 0b1100): "amoand.w",
            (0b101111, 0b10, 0b1000): "amoor.w",
            (0b101111, 0b10, 0b100): "amoxor.w",
            (0b101111, 0b10, 0b10100): "amomax.w",
            (0b101111, 0b10, 0b10000): "amomin.w",
            (0b101111, 0b10, 0b11100): "amomaxu.w",
            (0b101111, 0b10, 0b11000): "amominu.w",
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

        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3, self.bitfields.funct7 if self.bitfields.opcode != 0b101111 else self.bitfields.funct5), "unknown")
        self.destination_register = utils.format_register(self.bitfields.rd)
        self.source_register_1 = utils.format_register(self.bitfields.rs1)
        self.source_register_2 = utils.format_register(self.bitfields.rs2)

        if self.bitfields.aqrl == 0b11:
            self.mnemonic += ".aqrl"
        elif self.bitfields.aqrl == 0b10:
            self.mnemonic += ".aq"
        elif self.bitfields.aqrl == 0b01:
            self.mnemonic += ".rl"

        if self.bitfields.opcode != 0b101111:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_1}, {self.source_register_2}"
        else:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_2}, ({self.source_register_1})" if "lr.w" not in self.mnemonic else f"{self.mnemonic} {self.destination_register}, ({self.source_register_1})"
        return self.decoded

class JTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1101111,): "jal"
        }
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode,), "unknown")
        self.destination_register = utils.format_register(self.bitfields.rd)
        self.immediate = utils.twos_complement(self.bitfields.j_imm, 21)

        self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}"
        return self.decoded
    
class MiscTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1111, 0b0): "fence"
        }