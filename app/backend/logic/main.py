with open("./test_binaries/test0.bin", "rb") as file:
    data = file.read()
instructions = [data[i:i+4] for i in range(0, len(data), 4)]

opcode2type = {3: "I", 19: "I", 103: "I", 23: "U", 55: "U", 35: "S", 51: "R", 99: "B", 111: "J"}
itype2mnemonic = {3: "lb", 4: "lh", 5: "lw", 7: "lbu", 8: "lhu", 19: "addi", 20: "slli", 21: "slti", 22: "sltiu", 23: "xori", 24: "srli", 25: "ori", 26: "andi", 103: "jalr"}
stype2mnemonic = {(35, 0): "sb", (35, 1): "sh", (35, 2): "sw"}
rtype2mnemonic = {(51, 0, 0): "add", (51, 0, 32): "sub", (51, 1, 0): "sll", (51, 2, 0): "slt", (51, 3, 0): "sltu", (51, 4, 0): "xor", (51, 5, 0): "srl", (51, 5, 32): "sra", (51, 6, 0): "or", (51, 7, 0): "and"}
btype2mnemonic = {(99, 0): "beq", (99, 1): "bne", (99, 4): "blt", (99, 5): "bge", (99, 6): "bltu", (99, 7): "bgeu"}

def twos_complement(bin):
    bits = len(bin)
    val = int(bin, 2)
    if val >= 2**(bits-1):
        val -= 2**bits
    return val

output = []
labels = {}
address = 1000
for instr in instructions:
    instr = int.from_bytes(instr, "little")
    instr_str = f"{instr:032b}"
    opcode = instr_str[-7:]
    type = opcode2type[int(opcode, 2)]
    if type == "I":
        funct3 = instr_str[-15:-12]
        mnemonic = itype2mnemonic[int(funct3, 2) + int(opcode, 2)]
        rd = instr_str[-12:-7]
        destination_register = "x" + str(int(rd, 2))
        rs1 = instr_str[-20:-15]
        source_register_1 = "x" + str(int(rs1, 2))
        imm = instr_str[-32:-20]
        immediate = int(imm, 2)
        if mnemonic == "srli":
            immediate = int(imm[-5:], 2)
        mnemonic = "srai" if mnemonic == "srli" and int(imm[0:7], 2) == 32 else mnemonic
        if int(opcode, 2) == 3:
            output.append((address, f"{mnemonic} {destination_register}, {immediate}({source_register_1})\n"))
        else:
            output.append((address, f"{mnemonic} {destination_register}, {source_register_1}, {immediate}\n"))
    elif type == "U":
        mnemonic = "auipc" if int(opcode, 2) == 23 else "lui"
        rd = instr_str[-12:-7]
        destination_register = "x" + str(int(rd, 2))
        imm = instr_str[-32:-12]
        immediate = int(imm, 2)
        output.append((address, f"{mnemonic} {destination_register}, {immediate}\n"))
    elif type == "S":
        funct3 = instr_str[-15:-12]
        mnemonic = stype2mnemonic[(int(opcode, 2), int(funct3, 2))]
        rs1 = instr_str[-20:-15]
        source_register_1 = "x" + str(int(rs1, 2))
        rs2 = instr_str[-25:-20]
        source_register_2 = "x" + str(int(rs2, 2))
        imm = instr_str[-32:-25] + instr_str[-12:-7]
        immediate = int(imm, 2)
        output.append((address, f"{mnemonic} {source_register_2}, {immediate}({source_register_1})\n"))
    elif type == "R":
        funct3 = instr_str[-15:-12]
        funct7 = instr_str[-32:-25]
        mnemonic = rtype2mnemonic[(int(opcode, 2), int(funct3, 2), int(funct7, 2))]
        rd = instr_str[-12:-7]
        destination_register = "x" + str(int(rd, 2))
        rs1 = instr_str[-20:-15]
        source_register_1 = "x" + str(int(rs1, 2))
        rs2 = instr_str[-25:-20]
        source_register_2 = "x" + str(int(rs2, 2))
        output.append((address, f"{mnemonic} {destination_register}, {source_register_1}, {source_register_2}\n"))
    elif type == "B":
        funct3 = instr_str[-15:-12]
        mnemonic = btype2mnemonic[(int(opcode, 2), int(funct3, 2))]
        rs1 = instr_str[-20:-15]
        source_register_1 = "x" + str(int(rs1, 2))
        rs2 = instr_str[-25:-20]
        source_register_2 = "x" + str(int(rs2, 2))
        imm = instr_str[0] + instr_str[-8] + instr_str[-31:-25] + instr_str[-12:-8]
        immediate = twos_complement(imm)
        label = "label_" + str(len(labels))
        labels[address + immediate] = label
        output.append((address, f"{mnemonic} {source_register_1}, {source_register_2}, {label}\n"))
    elif type == "J":
        mnemonic = "jal"
        rd = instr_str[-12:-7]
        destination_register = int(rd, 2)
        imm = instr_str[0] + instr_str[-15:-7] + instr_str[-16] + instr_str[1:11]
        immediate = int(imm, 2)
        label = "label_" + str(len(labels))
        labels[address + immediate] = label
        output.append((address, f"{mnemonic} {destination_register}, {label}\n"))
    address += 4

with open("./output/output.s", "w") as file:
    for instruction in output:
        if instruction[0] in labels:
            file.write(labels[instruction[0]] + ":\n")
        file.write(str(instruction[0]) + "\t" + instruction[1])