.section .text
.global _start

_start:
    fcvt.l.d x10, f0
    fcvt.lu.d x11, f0
    fcvt.d.l f1, x12
    fcvt.d.lu f2, x13
    fmv.x.d x14, f0
    fmv.d.x f3, x15
    