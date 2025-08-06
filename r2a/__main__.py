import argparse
from r2a import Disassembler

def main():
    parser = argparse.ArgumentParser(description="RISC-V Disassembler CLI")
    parser.add_argument("input", help="Path to the binary file to disassemble")
    parser.add_argument("output", help="Path to the assembly file to output")

    args = parser.parse_args()
    Disassembler.decode_binary_file(args.input, args.output)

if __name__ == "__main__":
    main()