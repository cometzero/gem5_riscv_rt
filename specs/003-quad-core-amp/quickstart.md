# Quickstart: Quad Core AMP Zephyr

**Feature**: Quad Core AMP Zephyr
**Status**: Draft

## Prerequisites

1. **Build gem5**: Ensure `build/RISCV/gem5.opt` is built.
2. **Zephyr Binaries**: You need 4 Zephyr ELF files (can be the same file 4 times for testing).

## Running the Simulation

```bash
# Example: Running with 4 copies of the same hello_world kernel
./build/RISCV/gem5.opt \
    configs/riscv_rt/fs_quad_amp.py \
    --kernels zephyr.elf,zephyr.elf,zephyr.elf,zephyr.elf
```

## Verifying Output

Check the terminal outputs for each core:

```bash
cat m5out/system.pc.com_1.device # Core 0
cat m5out/system.pc.com_2.device # Core 1
cat m5out/system.pc.com_3.device # Core 2
cat m5out/system.pc.com_4.device # Core 3
```

You should see the Zephyr boot banner in each file.
