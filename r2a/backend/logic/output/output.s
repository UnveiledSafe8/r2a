.section .text
.globl _start

_start:
	addi x1, x0, 0
	addi x2, x0, -1
	addi x3, x0, 2047
	addi x4, x0, -2048
	add x5, x1, x2
	sub x6, x3, x4
	xor x7, x5, x6
	or x8, x5, x7
	and x9, x6, x7
	sw x5, 4(x0)
	lw x10, -4(x0)
	addiw x11, x0, 123
	addw x12, x11, x3
	subw x13, x12, x4
	slliw x14, x3, 0
	slliw x15, x3, 31
	srliw x16, x14, 1
	srliw x17, x15, 31
	mul.rl x18, x1, x2
	mulh.rl x19, x1, x2
	mulsu.rl x20, x1, x2
	div.rl x21, x2, x1
	divu.rl x22, x2, x1
	rem.rl x23, x2, x1
	remu.rl x24, x2, x1
	lr.w x30, (x0)
	sc.w x31, x2, (x0)
	amoswap.w x5, x6, (x0)
	amoadd.w x6, x7, (x0)
	amoxor.w.aq x7, x8, (x0)
	amoand.w.rl x8, x9, (x0)
	amoor.w.aqrl x9, x10, (x0)
	amomin.w x10, x11, (x0)
	amomax.w x11, x12, (x0)
	amominu.w x12, x13, (x0)
	amomaxu.w x13, x14, (x0)
	beq x3, x4, label_1168
	bne x3, x4, label_1172
	blt x3, x4, label_1176
	bge x3, x4, label_1180
	jal x0, label_1184
	jalr x1, x2, 0
label_1168:
	addi x25, x0, 1
label_1172:
	addi x26, x0, 2
label_1176:
	addi x27, x0, 3
label_1180:
	addi x28, x0, 4
label_1184:
	addi x0, x0, 0
	ecall x0, x0, 0
label_1192:
	addi x29, x0, -1
	jal x0, label_1192
