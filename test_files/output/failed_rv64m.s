.section .text
.globl _start

_start:
	addi x1, x0, 2
	addi x2, x0, -3
	addi x3, x0, 0
	addiw x4, x0, -1
	slli x4, x4, 31
	addi x4, x4, -1
	addiw x5, x0, -1
	slli x5, x5, 31
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
