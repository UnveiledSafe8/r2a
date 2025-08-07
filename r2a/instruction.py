from .utils import twos_complement
from .bit_fields import BitFieldDecoder

class Instruction:
    def __init__(self, raw_binary):
        self.raw_binary = raw_binary
        self.bitfields = BitFieldDecoder(raw_binary)
        self.decoded = None

        self.mnemonic = None
        self.immediate = None
        self.rounding_mode = None
        self.destination_register = None
        self.source_register_1 = None
        self.source_register_2 = None
        self.source_register_3 = None

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
        
    def format_register(self, register):
        return f"x{register}"
    
    def decode(self):
        self.decoded = "unknown"
        return self.decoded

    @classmethod
    def from_binary(cls, raw_bytes):
        opcodeRegistry = {
                0b11: ITypeInstruction,
                0b111: ITypeInstruction,
                0b10011: ITypeInstruction,
                0b11011: ITypeInstruction,
                0b1100111: ITypeInstruction,
                0b1110011: ITypeInstruction,
                0b10111: UTypeInstruction,
                0b110111: UTypeInstruction,
                0b100011: STypeInstruction,
                0b100111: STypeInstruction,
                0b110011: RTypeInstruction,
                0b111011: RTypeInstruction,
                0b101111: RTypeInstruction,
                0b1010011: RTypeInstruction,
                0b1100011: BTypeInstruction,
                0b1101111: JTypeInstruction,
                0b1000011: R4TypeInstruction,
                0b1000111: R4TypeInstruction,
                0b1001011: R4TypeInstruction,
                0b1001111: R4TypeInstruction,
                0b1111: MiscTypeInstruction
            }
        
        raw_binary = int.from_bytes(raw_bytes, "little")

        if len(raw_bytes) == 4:
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
            (0b111, 0b10): "flw",
            (0b111, 0b11): "fld",
            (0b111, 0b100): "flq",
            (0b10011, 0b0): "addi",
            (0b10011, 0b1): "slli", #If funct7 isnt exactly 0 or 0b10000, then we know that 64-bit version is the likely candidate. However, if we do get funct7==0, then 64-bit or 32-bit is valid. But this is irrelevant since shamt is clearly not using upper bit if originally 64-bit so we can treat the instruction as 32-bit
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
            (0b1110011, 0b0): "ecall",
            (0b1110011, 0b1): "csrrw",
            (0b1110011, 0b10): "csrrs",
            (0b1110011, 0b11): "csrrc",
            (0b1110011, 0b101): "csrrwi",
            (0b1110011, 0b110): "csrrsi",
            (0b1110011, 0b111): "csrrci"
        }
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        if self.mnemonic in ("slli", "srli", "slliw", "srliw") and (self.bitfields.funct7 == 0 or self.bitfields.funct7 == 0b100000):
            self.immediate = self.bitfields.i_imm & 0b11111
        elif self.mnemonic in ("slli", "srli", "slliw", "srliw") and (self.bitfields.funct7 & 0b1):
            self.immediate = self.bitfields.i_imm & 0b111111
        elif self.bitfields.opcode == 0b1110011 and self.bitfields.funct3 >= 0b101:
            self.immediate = self.bitfields.rs1
        else:
            self.immediate = twos_complement(self.bitfields.i_imm, 12)
        self.control_source_register = self.bitfields.csr
        self.destination_register = self.format_register(self.bitfields.rd) if self.mnemonic not in ("flw", "fld", "flq") else f"f{self.bitfields.rd}"
        self.source_register_1 = self.format_register(self.bitfields.rs1)

        if self.mnemonic == "srli" and self.bitfields.funct7 == 0b100000 or self.bitfields.funct7 == 0b100001:
            self.mnemonic = "srai"
        elif self.mnemonic == "srliw" and self.bitfields.funct7 == 0b100000:
            self.mnemonic = "sraiw"
        elif self.mnemonic == "ecall" and (self.bitfields.rd != 0 or self.bitfields.rs1 != 0):
            self.mnemonic = "unknown"
        elif self.mnemonic == "ecall" and self.bitfields.i_imm == 0b1:
            self.mnemonic = "ebreak"

        if self.bitfields.opcode in (0b11, 0b111):
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}({self.source_register_1})"
        elif self.mnemonic in ("ecall", "ebreak"):
            self.decoded = self.mnemonic
        elif self.bitfields.opcode == 0b1110011:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.control_source_register}, {self.source_register_1 if self.bitfields.funct3 < 0b101 else self.immediate}"
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
         self.destination_register = self.format_register(self.bitfields.rd)
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
            (0b100011, 0b10): "sw",
            (0b100111, 0b10): "fsw",
            (0b100111, 0b11): "fsd",
            (0b100111, 0b100): "fsq"
        }
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        self.source_register_1 = self.format_register(self.bitfields.rs1)
        self.source_register_2 = self.format_register(self.bitfields.rs2) if self.mnemonic not in ("fsw", "fsd", "fsq") else f"f{self.bitfields.rs2}"
        self.immediate = twos_complement(self.bitfields.s_imm, 12)

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
        self.source_register_1 = self.format_register(self.bitfields.rs1)
        self.source_register_2 = self.format_register(self.bitfields.rs2)
        self.immediate = twos_complement(self.bitfields.b_imm, 13)

        self.decoded = f"{self.mnemonic} {self.source_register_1}, {self.source_register_2}, {self.immediate}"
        return self.decoded


class RTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b101111, None, 0b10): "lr",
            (0b101111, None, 0b11): "sc",
            (0b101111, None, 0b1): "amoswap",
            (0b101111, None, 0b0): "amoadd",
            (0b101111, None, 0b1100): "amoand",
            (0b101111, None, 0b1000): "amoor",
            (0b101111, None, 0b100): "amoxor",
            (0b101111, None, 0b10100): "amomax",
            (0b101111, None, 0b10000): "amomin",
            (0b101111, None, 0b11100): "amomaxu",
            (0b101111, None, 0b11000): "amominu",
            (0b110011, 0b0, 0b0): "add",
            (0b110011, 0b0, 0b1): "mul",
            (0b110011, 0b1, 0b1): "mulh",
            (0b110011, 0b10, 0b1): "mulhsu",
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
            (0b111011, 0b101, 0b100000): "sraw",
            (0b111011, 0b0, 0b1): "mulw",
            (0b111011, 0b100, 0b1): "divw",
            (0b111011, 0b101, 0b1): "divuw",
            (0b111011, 0b110, 0b1): "remw",
            (0b111011, 0b111, 0b1): "remuw",
            (0b1010011, 0b0, 0b100): "fsgnj",
            (0b1010011, 0b1, 0b100): "fsgnjn",
            (0b1010011, 0b10, 0b100): "fsgnjx",
            (0b1010011, 0b0, 0b101): "fmin",
            (0b1010011, 0b1, 0b101): "fmax",
            (0b1010011, 0b0, 0b10100): "fle",
            (0b1010011, 0b1, 0b10100): "flt",
            (0b1010011, 0b10, 0b10100): "feq"
        }

        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3 if self.bitfields.opcode not in (0b101111,) else None, self.bitfields.funct7 if self.bitfields.opcode not in (0b101111, 0b1010011) else self.bitfields.funct5), "unknown")
        self.destination_register = self.format_register(self.bitfields.rd) if self.bitfields.opcode not in (0b1010011,) or self.mnemonic in ("fle", "flt", "feq") else f"f{self.bitfields.rd}"
        self.source_register_1 = self.format_register(self.bitfields.rs1) if self.bitfields.opcode not in (0b1010011,) else f"f{self.bitfields.rs1}"
        self.source_register_2 = self.format_register(self.bitfields.rs2) if self.bitfields.opcode not in (0b1010011,) else f"f{self.bitfields.rs2}"

        if self.bitfields.opcode == 0b101111:
            if self.bitfields.funct3 == 0b10:
                self.mnemonic += ".w"
            elif self.bitfields.funct3 == 0b11:
                self.mnemonic += ".d"

            if self.bitfields.aqrl == 0b11:
                self.mnemonic += ".aqrl"
            elif self.bitfields.aqrl == 0b10:
                self.mnemonic += ".aq"
            elif self.bitfields.aqrl == 0b01:
                self.mnemonic += ".rl"
        elif self.bitfields.opcode == 0b1010011:
            if self.bitfields.fmt == 0b11:
                self.mnemonic += ".q"
            elif self.bitfields.fmt == 0b10:
                self.mnemonic += ".h"
            elif self.bitfields.fmt == 0b01:
                self.mnemonic += ".d"
            else:
                self.mnemonic += ".s"

        if self.bitfields.opcode == 0b101111:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_2}, ({self.source_register_1})" if "lr" not in self.mnemonic else f"{self.mnemonic} {self.destination_register}, ({self.source_register_1})"
        else:
            self.decoded = f"{self.mnemonic} {self.destination_register}, {self.source_register_1}, {self.source_register_2}"
        return self.decoded

class JTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1101111,): "jal"
        }
        
        self.mnemonic = mnemonics.get((self.bitfields.opcode,), "unknown")
        self.destination_register = self.format_register(self.bitfields.rd)
        self.immediate = twos_complement(self.bitfields.j_imm, 21)

        self.decoded = f"{self.mnemonic} {self.destination_register}, {self.immediate}"
        return self.decoded
    
class R4TypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1000011,): "fmadd",
            (0b1000111,): "fmsub",
            (0b1001011,): "fnmsub",
            (0b1001111,): "fnmadd"
        }

        self.mnemonic = mnemonics.get((self.bitfields.opcode,), "unknown")

        if self.bitfields.fmt == 0b11:
            self.mnemonic += ".q"
        elif self.bitfields.fmt == 0b10:
            self.mnemonic += ".h"
        elif self.bitfields.fmt == 0b01:
            self.mnemonic += ".d"
        else:
            self.mnemonic += ".s"

        self.destination_register = f"f{self.bitfields.rd}"
        self.source_register_1 = f"f{self.bitfields.rs1}"
        self.source_register_2 = f"f{self.bitfields.rs2}"
        self.source_register_3 = f"f{self.bitfields.rs3}"
        if self.bitfields.rm == 0b0:
            self.rounding_mode = "rne"
        elif self.bitfields.rm == 0b1:
            self.rounding_mode = "rtz"
        elif self.bitfields.rm == 0b10:
            self.rounding_mode = "rdn"
        elif self.bitfields.rm == 0b11:
            self.rounding_mode = "rup"
        elif self.bitfields.rm == 0b100:
            self.rounding_mode = "rmm"
        elif self.bitfields.rm == 0b111:
            self.rounding_mode = "dyn"

        self.decoded = f"{self.mnemonic}  {self.destination_register}, {self.source_register_1}, {self.source_register_2}, {self.source_register_3}, {self.rounding_mode}"
        return self.decoded
    
class MiscTypeInstruction(Instruction):
    def decode(self):
        if self.decoded:
            return self.decoded
        
        mnemonics = {
            (0b1111, 0b0): "fence",
            (0b1111, 0b1): "fence.i"
        }

        self.mnemonic = mnemonics.get((self.bitfields.opcode, self.bitfields.funct3), "unknown")
        self.predicate = ""
        self.succesor = ""

        if self.bitfields.pred & 0b1000:
            self.predicate += "i"
        if self.bitfields.pred & 0b100:
            self.predicate += "o"
        if self.bitfields.pred & 0b10:
            self.predicate += "r"
        if self.bitfields.pred & 0b1:
            self.predicate += "w"

        if self.bitfields.succ & 0b1000:
            self.succesor += "i"
        if self.bitfields.succ & 0b100:
            self.succesor += "o"
        if self.bitfields.succ & 0b10:
            self.succesor += "r"
        if self.bitfields.succ & 0b1:
            self.succesor += "w"

        if self.mnemonic in ("fence.i",):
            self.decoded = f"{self.mnemonic}"
        else:
            self.decoded = f"{self.mnemonic} {self.predicate}, {self.succesor}"

        return self.decoded
    