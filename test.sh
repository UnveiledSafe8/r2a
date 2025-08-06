#!/bin/bash

ASSEMBLER="riscv64-unknown-elf-as"
OBJCOPY="riscv64-unknown-elf-objcopy"

rm -rf test_files/output/*

for INPUT_ASM in test_files/input/*.s; do
    $ASSEMBLER "$INPUT_ASM" -o "test_files/input/temp.o" || {
        echo "Assembly failed for $INPUT_ASM"
        continue
    }

    $OBJCOPY -O binary test_files/input/temp.o "test_files/input/temp.bin"

    python3 -m r2a test_files/input/temp.bin test_files/output/temp.s || {
        echo "Disassembly failed for $INPUT_ASM"
        rm -f test_files/input/temp.o test_files/input/temp.bin
        continue
    }

    $ASSEMBLER test_files/output/temp.s -o "test_files/output/temp.o" || {
        echo "Assembly failed for $INPUT_ASM"
        rm -f test_files/input/temp.o test_files/input/temp.bin
        mv test_files/output/temp.s test_files/output/failed_$(basename "$INPUT_ASM")
        continue
    }

    $OBJCOPY -O binary test_files/output/temp.o test_files/output/temp.bin

    cmp -l test_files/input/temp.bin test_files/output/temp.bin
    if [ $? -ne 0 ]; then
        echo "Test failed: binaries differ for $INPUT_ASM"
        mv test_files/output/temp.s test_files/output/failed_$(basename "$INPUT_ASM")
    fi

    rm -f test_files/input/temp.o test_files/input/temp.bin test_files/output/temp.o test_files/output/temp.bin test_files/output/temp.s
done