def twos_complement(value, bits):
    if value & (1 << (bits - 1)):
        value -= (1 << bits)
    return value

def format_register(register):
    return f"x{register}"