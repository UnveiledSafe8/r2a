.section .text
.globl _start

_start:
    addi x1, x0, 0
    addi x2, x0, 1
    addi x3, x0, -1
    addi x4, x0, 2047
    addi x5, x0, -2048

    add x6, x1, x2
    sub x7, x3, x4
    xor x8, x6, x7
    or x9, x6, x8
    and x10, x7, x8

    slli x11, x1, 0
    slli x12, x1, 31
    srli x13, x12, 0
    srli x14, x12, 31
    srai x15, x12, 0
    srai x16, x12, 31

    sw x6, 0(x0)
    lw x17, 0(x0)
    sb x6, 1(x0)
    lb x18, 1(x0)
    sh x6, 2(x0)
    lh x19, 2(x0)

    lui x20, 0x12345
    auipc x21, 0x12345

    jal x22, label_jal
    jalr x23, 0(x1)
    beq x1, x2, label_beq
    bne x1, x2, label_bne
    blt x1, x2, label_blt
    bge x1, x2, label_bge
    bltu x1, x2, label_bltu
    bgeu x1, x2, label_bgeu

label_jal:
    nop

label_beq:
    nop

label_bne:
    nop

label_blt:
    nop

label_bge:
    nop

label_bltu:
    nop

label_bgeu:
    nop
    jal x12, label_jal
    ecall
    ebreak
    