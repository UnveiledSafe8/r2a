from .utils import twos_complement
from .bit_fields import BitFieldDecoder
from .instruction_data import INSTRUCTION_SET

class Decoder:
    def __init__(self, raw_bytes):
        self.raw_binary = int.from_bytes(raw_bytes, "little")
        self.bitfields = BitFieldDecoder(self.raw_binary)
        self.decoded = None

        self.mnemonic = None
        self.immediate = None

    def __str__(self):
        return self.decode()
    
    def __int__(self):
        return self.raw_binary
    
    def __eq__(self, other):
        if isinstance(other, int):
            return self.raw_binary == other
        elif isinstance(other, Decoder):
            return self.raw_binary == other.raw_binary
        elif isinstance(other, str):
            return self.raw_binary == other.encode("utf-8")
        else:
            return False
    
    def decode(self):
        if self.decoded:
            return self.decoded
        
        DECODING_SCHEME = {
            "I": self._decode_i_type,
            "U": self._decode_u_type,
            "S": self._decode_s_type,
            "B": self._decode_b_type,
            "R": self._decode_r_type,
            "J": self._decode_j_type,
            "R4": self._decode_r4_type,
            "Misc": self._decode_misc_type
        }
        
        self.instruction = None
        curr_level = INSTRUCTION_SET

        while not self.instruction:
            field = curr_level.get("_next_field")
            if field:
                if field == "opcode":
                    field = self.bitfields.opcode
                elif field == "funct3":
                    field = self.bitfields.funct3
                elif field == "funct5":
                    field = self.bitfields.funct5
                elif field == "funct7":
                    field = self.bitfields.funct7
                elif field == "imm":
                    field = self.bitfields.i_imm
                else:
                    break
                curr_level = curr_level["_nodes"][field]
            else:
                self.instruction = curr_level.get("_instruction")

        DECODING_SCHEME[self.instruction["instr_type"]]()

        return self.decoded
    
    def _decode_i_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        if self.mnemonic in ("slli", "srli", "srai") and "funct6" not in self.instruction:
            self.immediate = self.bitfields.i_imm & 0b11111
        elif self.mnemonic in ("slli", "srli", "srai", "slliw", "srliw", "sraiw"):
            self.immediate = self.bitfields.i_imm & 0b111111
        else:
            self.immediate = twos_complement(self.bitfields.i_imm, 12)

        if self.bitfields.opcode in (0b11, 0b111):
            self.decoded = f"{self.mnemonic} {'x' if self.bitfields.opcode != 0b111 else 'f'}{self.bitfields.rd}, {self.immediate}(x{self.bitfields.rs1})"
        elif self.mnemonic in ("ecall", "ebreak"):
            self.decoded = self.mnemonic
        elif self.bitfields.opcode == 0b1110011:
            self.decoded = f"{self.mnemonic} x{self.bitfields.rd}, {self.bitfields.csr}, {'x' if self.bitfields.funct3 < 0b101 else ''}{self.bitfields.rs1}"
        else:                                                                                                                                                                                   
            self.decoded = f"{self.mnemonic} x{self.bitfields.rd}, x{self.bitfields.rs1}, {self.immediate}"

    def _decode_u_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        self.immediate = self.bitfields.u_imm

        self.decoded = f"{self.mnemonic} x{self.bitfields.rd}, {self.immediate}"

    def _decode_s_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        self.immediate = twos_complement(self.bitfields.s_imm, 12)

        self.decoded = f"{self.mnemonic} {'x' if self.instruction['opcode'] != 0b100111 else 'f'}{self.bitfields.rs2}, {self.immediate}(x{self.bitfields.rs1})"

    def _decode_b_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        self.immediate = twos_complement(self.bitfields.b_imm, 13)

        self.decoded = f"{self.mnemonic} x{self.bitfields.rs1}, x{self.bitfields.rs2}, {self.immediate}"

    def _decode_r_type(self):
        self.mnemonic = self.instruction["mnemonic"]
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
            if ("fcvt" in self.mnemonic and self.instruction["funct5"] == 0b11000) or ("fmv" in self.mnemonic and self.instruction["funct5"] == 0b11110):
                if self.bitfields.rs2 == 0b0:
                    self.mnemonic += ".w" if ("fmv" not in self.mnemonic or self.bitfields.fmt == 0b0) else ".d"
                elif self.bitfields.rs2 == 0b1:
                    self.mnemonic += ".wu"
                elif self.bitfields.rs2 == 0b10:
                    self.mnemonic += ".l"
                elif self.bitfields.rs2 == 0b11:
                    self.mnemonic += ".lu"
            if "fmv" in self.mnemonic:
                self.mnemonic += ".x"
            else:
                if self.bitfields.fmt == 0b11:
                    self.mnemonic += ".q"
                elif self.bitfields.fmt == 0b10:
                    self.mnemonic += ".h"
                elif self.bitfields.fmt == 0b01:
                    self.mnemonic += ".d"
                else:
                    self.mnemonic += ".s"
            if ("fcvt" in self.mnemonic and (self.instruction["funct5"] == 0b11010 or self.instruction["funct5"] == 0b1000)) or ("fmv" in self.mnemonic and self.instruction["funct5"] == 0b11100):
                if self.bitfields.rs2 == 0b0:
                    if "fmv" in self.mnemonic and self.bitfields.fmt == 0b1:
                        self.mnemonic += ".d"
                    elif "fcvt" in self.mnemonic and self.instruction["funct5"] == 0b1000:
                        self.mnemonic += ".s"
                    else:
                        self.mnemonic += ".w"
                elif self.bitfields.rs2 == 0b1:
                    self.mnemonic += ".wu" if ("fcvt" not in self.mnemonic or self.instruction["funct5"] != 0b1000) else ".d"
                elif self.bitfields.rs2 == 0b10:
                    self.mnemonic += ".l"
                elif self.bitfields.rs2 == 0b11:
                    self.mnemonic += ".lu"

        if self.instruction["opcode"] == 0b101111:
            self.decoded = f"{self.mnemonic} x{self.bitfields.rd}, x{self.bitfields.rs2}, (x{self.bitfields.rs1})" if "lr" not in self.mnemonic else f"{self.mnemonic} x{self.bitfields.rd}, (x{self.bitfields.rs1})"
        elif "fsqrt" in self.instruction["mnemonic"] or "fcvt" == self.instruction["mnemonic"] or "fclass" in self.instruction["mnemonic"] or "fmv" in self.instruction["mnemonic"]:
            self.decoded = f"{self.mnemonic} {'f' if self.bitfields.funct5 not in (0b11000, 0b11100) else 'x'}{self.bitfields.rd}, {'f' if self.bitfields.funct5 not in (0b11010, 0b11110) else 'x'}{self.bitfields.rs1}"
        else:
            self.decoded = f"{self.mnemonic} {'x' if self.instruction['mnemonic'] in ('fle', 'flt', 'feq') or self.instruction['opcode'] != 0b1010011 else 'f'}{self.bitfields.rd}, {'x' if self.instruction['opcode'] != 0b1010011 else 'f'}{self.bitfields.rs1}, {'x' if self.instruction['opcode'] != 0b1010011 else 'f'}{self.bitfields.rs2}"

    def _decode_j_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        self.immediate = twos_complement(self.bitfields.j_imm, 21)

        self.decoded = f"{self.mnemonic} x{self.bitfields.rd}, {self.immediate}"

    def _decode_r4_type(self):
        self.mnemonic = self.instruction["mnemonic"]

        if self.bitfields.fmt == 0b11:
            self.mnemonic += ".q"
        elif self.bitfields.fmt == 0b10:
            self.mnemonic += ".h"
        elif self.bitfields.fmt == 0b01:
            self.mnemonic += ".d"
        else:
            self.mnemonic += ".s"

        if self.bitfields.rm == 0b0:
            rounding_mode = "rne"
        elif self.bitfields.rm == 0b1:
            rounding_mode = "rtz"
        elif self.bitfields.rm == 0b10:
            rounding_mode = "rdn"
        elif self.bitfields.rm == 0b11:
            rounding_mode = "rup"
        elif self.bitfields.rm == 0b100:
            rounding_mode = "rmm"
        elif self.bitfields.rm == 0b111:
            rounding_mode = "dyn"

        self.decoded = f"{self.mnemonic} f{self.bitfields.rd}, f{self.bitfields.rs1}, f{self.bitfields.rs2}, f{self.bitfields.rs3}, {rounding_mode}"

    def _decode_misc_type(self):
        self.mnemonic = self.instruction["mnemonic"]
        predicate = ""
        succesor = ""

        if self.bitfields.pred & 0b1000:
            predicate += "i"
        if self.bitfields.pred & 0b100:
            predicate += "o"
        if self.bitfields.pred & 0b10:
            predicate += "r"
        if self.bitfields.pred & 0b1:
            predicate += "w"

        if self.bitfields.succ & 0b1000:
            succesor += "i"
        if self.bitfields.succ & 0b100:
            succesor += "o"
        if self.bitfields.succ & 0b10:
            succesor += "r"
        if self.bitfields.succ & 0b1:
            succesor += "w"

        if self.mnemonic in ("fence.i",):
            self.decoded = f"{self.mnemonic}"
        else:
            self.decoded = f"{self.mnemonic} {predicate}, {succesor}"
