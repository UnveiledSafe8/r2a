.section .text
.globl _start

_start:
    addiw x1, x0, 0
    addiw x2, x0, 1
    addiw x3, x0, -1
    addw x4, x1, x2
    subw x5, x4, x3
    slliw x6, x1, 0
    slliw x7, x1, 31
    srliw x8, x7, 0
    srliw x9, x7, 31
    sraiw x10, x7, 0
    sraiw x11, x7, 31
    mulw x12, x4, x5
    divw x13, x5, x1
    divuw x14, x5, x1
    remw x15, x5, x1
    remuw x16, x5, x1

    add x17, x1, x2
    sub x18, x4, x5
    sll x19, x17, x2
    srl x20, x19, x2
    sra x21, x19, x2
    and x22, x17, x18
    or x23, x19, x20
    xor x24, x21, x22

    slli x25, x1, 0
    slli x26, x1, 63
    srli x27, x26, 0
    srli x28, x26, 63
    srai x29, x26, 0
    srai x30, x26, 63

    sd x17, 0(x0)
    ld x31, 0(x0)
    sw x1, 0(x0)
    lw x2, 0(x0)

    jal x1, label_jal
    jalr x2, 0(x3)
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
    jal x3, label_jal
    ecall
    ebreak
    