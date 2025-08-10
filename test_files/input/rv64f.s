.section .text
.global _start

_start:
    fcvt.s.l  f1, x10
    fcvt.s.lu f2, x11
    fcvt.l.s  x12, f0
    fcvt.lu.s x13, f0
