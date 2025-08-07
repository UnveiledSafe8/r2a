.section .text
.global _start

_start:
    fld    f1, 8(x1)
    fsd    f4, 24(x1)
    fmadd.d f4, f1, f2, f3, rne
    fmsub.d f5, f1, f2, f3, rtz
    fnmadd.d f6, f1, f2, f3, rdn
    fnmsub.d f6, f1, f2, f3, dyn
    fsgnj.d   f7, f1, f2
    fsgnjn.d  f8, f1, f2
    fsgnjx.d  f9, f1, f2
    fmin.d    f10, f1, f2
    fmax.d    f11, f1, f2
    flt.d   x15, f3, f4
    feq.d   x16, f3, f4
    fle.d   x17, f3, f4
