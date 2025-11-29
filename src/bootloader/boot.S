    .section .text
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
    j loop

core0:
    li t0, 0x90000000
    jr t0
core1:
    li t0, 0x90100000
    jr t0
core2:
    li t0, 0x90200000
    jr t0
core3:
    li t0, 0x90300000
    jr t0

loop:
    wfi
    j loop
