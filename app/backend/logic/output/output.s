label_0:
1000	addi x5, x0, 0
1004	lw x6, 0(x5)
1008	lui x7, 23
1012	sw x8, 0(x7)
1016	add x18, x8, x6
1020	srai x4, x6, 5
1024	beq x0, x7, label_0
