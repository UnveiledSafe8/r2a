import instruction

def decode_binary_file(path):
    with open(path, "rb") as file:
        data = file.read()

    compressed = True
    decoded = []
    labels = {}
    address = 1000
    for index in range(0, len(data), 2):
        if compressed:
            raw_bytes = data[index:index+2]
            raw_bits = int.from_bytes(raw_bytes, "little")
            if (raw_bits & 0b11) == 0b11:
                compressed = False
                continue
        else:
            raw_bytes = data[index-2:index+2]
            compressed = True

        instr = instruction.Instruction.from_binary(raw_bytes)
        command = instr.decode()

        if command == "unknown" and compressed:
            compressed = False
            continue

        if instr.mnemonic in ("jal", "beq", "bne", "blt", "bge", "bltu", "bgeu"):
            target = instr.immediate + address
            if target not in labels:
                labels[target] = "label_" + str(target)
            command = command.replace(str(instr.immediate), labels[target])
        decoded.append((address, command))
        address += 4
        compressed = True

    with open("./output/output.s", "w") as file:
        file.write(".section .text\n.globl _start\n\n_start:\n")
        for address, instr in decoded:
            if address in labels:
                file.write(labels[address] + ":\n")
            file.write("\t" + instr + "\n")

decode_binary_file("./test_binaries/binaries/test1.bin")