.section .text
.globl _start

_start:
    lr.w x1, (x12)
    sc.w x2, x1, (x12)
    amoswap.w x3, x1, (x12)
    amoadd.w x4, x2, (x12)
    amoxor.w x5, x3, (x12)
    amoand.w x6, x4, (x12)
    amoor.w x7, x5, (x12)
    amomax.w x8, x6, (x12)
    amomin.w x9, x7, (x12)
    amomaxu.w x10, x8, (x12)
    amominu.w x11, x9, (x12)
    