.section .data

.section .text
.globl _start

_start:
    csrrw x1, 0x300, x2
    csrrs x3, 0x305, x4
    csrrc x5, 0x341, x6

    csrrwi x7, 0x300, 1
    csrrsi x8, 0x305, 0xF
    csrrci x9, 0x341, 0x1F

    ecall
