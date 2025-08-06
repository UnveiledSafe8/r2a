.section .text
.globl _start

_start:
    lr.d x1, (x12)
    sc.d x2, x1, (x12)
    amoswap.d x3, x1, (x12)
    amoadd.d x4, x2, (x12)
    amoxor.d x5, x3, (x12)
    amoand.d x6, x4, (x12)
    amoor.d x7, x5, (x12)
    amomax.d x8, x6, (x12)
    amomin.d x9, x7, (x12)
    amomaxu.d x10, x8, (x12)
    amominu.d x11, x9, (x12)
    