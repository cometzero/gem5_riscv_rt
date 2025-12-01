    .section .text
    .option norvc
    .global _start

_start:
    csrr a0, 0xf14
    li t0, 0
    beq a0, t0, core0
    li t0, 1
    beq a0, t0, core1
    li t0, 2
    beq a0, t0, core2
    li t0, 3
    beq a0, t0, core3
    li t0, 4
    beq a0, t0, core4
    li t0, 5
    beq a0, t0, core5
    li t0, 6
    beq a0, t0, core6
    li t0, 7
    beq a0, t0, core7
    # Should not happen for 8 cores
    j loop

core0:
    li t1, 0x10010000
    li t2, 48 # '0'
    sb t2, 0(t1)
    li t0, 0x90000000
    jr t0
core1:
    li t1, 0x10011000
    li t2, 49 # '1'
    sb t2, 0(t1)
    li t0, 0x90100000
    jr t0
core2:
    li t1, 0x10012000
    li t2, 50 # '2'
    sb t2, 0(t1)
    li t0, 0x90200000
    jr t0
core3:
    li t1, 0x10013000
    li t2, 51 # '3'
    sb t2, 0(t1)
    li t0, 0x90300000
    jr t0
core4:
    li t1, 0x10014000
    li t2, 83 # 'S'
    sb t2, 0(t1)
    li t0, 0x90400000
    jr t0
core5:
    li t0, 0x90400000
    jr t0
core6:
    li t0, 0x90400000
    jr t0
core7:
    li t0, 0x90400000
    jr t0

loop:
    wfi
    j loop
