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
    fadd.d  f14, f10, f11
    fsub.d  f15, f10, f11
    fmul.d  f16, f10, f11
    fdiv.d  f17, f10, f11
    fsqrt.d f18, f10
    fcvt.w.d x5, f0
    fcvt.d.w f1, x6
    fcvt.wu.d x7, f0
    fcvt.d.wu f2, x8
    fcvt.s.d f1, f2
    fcvt.d.s f4, f3
