# Data Model: Memory Map

## Physical Address Space (RISC-V 32-bit)

| Start Address | Size | Type | Description |
|---------------|------|------|-------------|
| `0x10000000` | 32MB | MMIO | VirtIO, UART, PLIC, CLINT (Standard QEMU/virt layout) |
| `0x20000000` | 32MB | Flash | NOR Flash (Boot ROM / Storage) |
| `0x80000000` | 2MB | SRAM | Fast On-Chip Memory (Critical Code/Data) |
| `0x80200000` | 126MB| DRAM | Main Memory (DDR3) or STT-MRAM |

## Zephyr Memory Layout (SRAM Boot)

| Section | Region | Address | Notes |
|---------|--------|---------|-------|
| `.text` | SRAM | `0x80000000` | Kernel and Application Code |
| `.rodata`| SRAM | `0x800xxxxx` | Read-only Data |
| `.data` | SRAM | `0x800xxxxx` | Initialized Data |
| `.bss` | SRAM | `0x800xxxxx` | Zero-initialized Data |
| `Heap` | DRAM | `0x80200000` | Dynamic Allocation |

## Zephyr Memory Layout (Mixed)

| Section | Region | Address | Notes |
|---------|--------|---------|-------|
| `.text` | DRAM | `0x80200000` | Main Kernel Code |
| `.sram_text`| SRAM | `0x80000000` | Critical Functions |
| `.sram_data`| SRAM | `0x800xxxxx` | Critical Data |
