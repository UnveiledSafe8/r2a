def twos_complement(bin):
    bits = bin.bit_length()
    if bin >= 2**(bits-1):
        bin -= 2**bits
    return bin

def format_register(register):
    return f"x{register}"