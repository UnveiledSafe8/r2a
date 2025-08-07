.section .data

.section .text
.globl _start

_start:
    fence
    fence r, w
    fence w, r
    fence r, r
    fence rw, rw

    fence.i
    fence.i

    fence rw, r
    fence r, rw
    fence w, w
    fence i, i

    ecall
    