class BitFieldDecoder:
    def __init__(self, raw_binary):
        self.raw_binary = raw_binary

    def get_bits(self, start, end):
        if start > end:
            start, end = end, start

        width = end - start + 1
        mask = (1 << width) - 1
        return (self.raw_binary >> start) & mask

    @property
    def opcode(self):
        return self.get_bits(0, 6)
    
    @property
    def funct3(self):
        return self.get_bits(12, 14)
    
    @property
    def funct5(self):
        return self.get_bits(27, 31)
    
    @property
    def funct7(self):
        return self.get_bits(25, 31)
    
    @property
    def aqrl(self):
        return self.get_bits(25, 26)
    
    @property
    def rd(self):
        return self.get_bits(7, 11)
    
    @property
    def rs1(self):
        return self.get_bits(15, 19)
    
    @property
    def rs2(self):
        return self.get_bits(20, 24)
    
    @property
    def i_imm(self):
        return self.get_bits(20, 31)
    
    @property
    def u_imm(self):
        return self.get_bits(12, 31)
    
    @property
    def s_imm(self):
        return (self.get_bits(25, 31) << 5) | (self.get_bits(7, 11))
    
    @property
    def b_imm(self):
        return (self.get_bits(31, 31) << 12) | (self.get_bits(7, 7) << 11) | (self.get_bits(25, 30) << 5) | (self.get_bits(8, 11) << 1)
    
    @property
    def j_imm(self):
        return (self.get_bits(31, 31) << 20) | (self.get_bits(12, 19) << 12) | (self.get_bits(20, 20) << 11) | (self.get_bits(21, 30) << 1)