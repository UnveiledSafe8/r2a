.section .text
.globl _start

_start:
    # RV32I Arithmetic (addi edge cases)
    addi x1, x0, 0             # add immediate zero (tests zero immediate)
    addi x2, x0, -1            # add immediate with negative one (tests negative immediates)
    addi x3, x0, 2047          # add immediate max positive 12-bit signed immediate
    addi x4, x0, -2048         # add immediate min negative 12-bit signed immediate

    add x5, x1, x2             # add registers (tests basic register addition)
    sub x6, x3, x4             # subtract registers (tests basic subtraction)
    xor x7, x5, x6             # bitwise XOR (tests bitwise operations)
    or x8, x5, x7              # bitwise OR (tests bitwise operations)
    and x9, x6, x7             # bitwise AND (tests bitwise operations)

    # RV32I Loads and Stores (different offsets)
    sw x5, 4(x0)               # store word with positive offset (tests store with offset)
    lw x10, -4(x0)             # load word with negative offset (tests load with offset)

    # RV64I Arithmetic (shift edge cases)
    addiw x11, x0, 123         # add immediate word (lower 32 bits sign-extended)
    addw x12, x11, x3          # add word registers (32-bit arithmetic on 64-bit arch)
    subw x13, x12, x4          # subtract word registers (32-bit arithmetic)
    slliw x14, x3, 0           # shift left logical immediate by 0 (edge case shift amount)
    slliw x15, x3, 31          # shift left logical immediate max shift (31 bits)
    srlw x16, x14, 1           # shift right logical word by 1 (tests shift right)
    srlw x17, x15, 31          # shift right logical word by max shift (31 bits)

    # Multiply Extension (M)
    mul x18, x1, x2            # multiply low 32 bits
    mulh x19, x1, x2           # multiply high signed * signed
    mulhsu x20, x1, x2         # multiply high signed * unsigned
    div x21, x2, x1            # signed division
    divu x22, x2, x1           # unsigned division
    rem x23, x2, x1            # signed remainder
    remu x24, x2, x1           # unsigned remainder

    # Atomic Memory Operations (A)
    lr.w x30, (x0)             # load-reserved (tests LR/SC mechanism)
    sc.w x31, x2, (x0)         # store-conditional (tests LR/SC mechanism)
    amoswap.w x5, x6, (x0)     # atomic swap
    amoadd.w x6, x7, (x0)      # atomic addition
    amoxor.w.aq x7, x8, (x0)   # atomic XOR with acquire
    amoand.w.rl x8, x9, (x0)   # atomic AND with release
    amoor.w.aqrl x9, x10, (x0) # atomic OR with acquire/release
    amomin.w x10, x11, (x0)    # atomic min signed
    amomax.w x11, x12, (x0)    # atomic max signed
    amominu.w x12, x13, (x0)   # atomic min unsigned
    amomaxu.w x13, x14, (x0)   # atomic max unsigned

    # Branches and Jumps (test label backward and forward)
    beq x3, x4, label_beq      # branch if equal (forward label)
    bne x3, x4, label_bne      # branch if not equal (forward label)
    blt x3, x4, label_blt      # branch if less than (forward label)
    bge x3, x4, label_bge      # branch if greater or equal (forward label)
    jal x0, label_end          # jump and link (unconditional jump forward)
    jalr x1, 0(x2)             # jump and link register (indirect jump)

label_beq:
    addi x25, x0, 1            # check branch target (beq)
label_bne:
    addi x26, x0, 2            # check branch target (bne)
label_blt:
    addi x27, x0, 3            # check branch target (blt)
label_bge:
    addi x28, x0, 4            # check branch target (bge)

label_end:
    nop                        # no operation (pseudo-instruction)
    ecall                      # environment call (system call)

label_back:
    addi x29, x0, -1           # backward branch target (tests backward branch jump)
    jal x0, label_back         # jump backward (tests backward jump)