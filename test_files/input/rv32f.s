.section .text
.global _start

_start:
    flw    f1, 0(x1)
    fsw    f4, 12(x1)
    fmadd.s f4, f1, f2, f3, rne
    fmsub.s f5, f1, f2, f3, rtz
    fnmadd.s f6, f1, f2, f3, rdn
    fnmsub.s f6, f1, f2, f3, dyn
    fsgnj.s   f7, f1, f2
    fsgnjn.s  f8, f1, f2
    fsgnjx.s  f9, f1, f2
    fmin.s    f10, f1, f2
    fmax.s    f11, f1, f2
    flt.s   x12, f1, f2
    feq.s   x13, f1, f2
    fle.s   x14, f1, f2
