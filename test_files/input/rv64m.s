.section .text
.globl _start

_start:
    li x1, 2
    li x2, -3
    li x3, 0
    li x4, 0x7FFFFFFFFFFFFFFF
    li x5, 0x8000000000000000

    mul x6, x1, x2
    mul x7, x1, x3
    mul x8, x4, x1

    mulh x9, x1, x2
    mulh x10, x4, x5

    mulhsu x11, x2, x4
    mulhsu x12, x1, x4

    mulw x13, x1, x2
    mulw x14, x4, x5

    div x15, x1, x2
    div x16, x2, x1
    div x17, x4, x5

    divu x18, x1, x2
    divu x19, x4, x1

    rem x20, x2, x1
    rem x21, x1, x2
    rem x22, x4, x5

    remu x23, x1, x2
    remu x24, x4, x1
