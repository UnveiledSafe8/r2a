.section .text
.globl _start

_start:
    li x1, 2
    li x2, -3
    li x3, 0
    li x4, 0x7FFFFFFF
    li x5, 0x80000000

    mul x6, x1, x2
    mul x7, x1, x3
    mul x8, x4, x1

    mulh x9, x1, x2
    mulh x10, x4, x5

    mulhsu x11, x2, x4
    mulhsu x12, x1, x4

    div x13, x1, x2
    div x14, x2, x1
    div x15, x4, x5

    divu x16, x1, x2
    divu x17, x4, x1

    rem x18, x2, x1
    rem x19, x1, x2
    rem x20, x4, x5

    remu x21, x1, x2
    remu x22, x4, x1
