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
    fadd.s  f4, f0, f1
    fsub.s  f5, f0, f1
    fmul.s  f6, f0, f1
    fdiv.s  f7, f0, f1
    fsqrt.s f8, f0
    fcvt.s.w  f1, x10
    fcvt.s.wu f2, x11
    fcvt.w.s  x12, f0
    fcvt.wu.s x13, f0
    fclass.s x10, f0
    fmv.x.w x11, f0
    fmv.w.x f1, x11
