# Quickstart: Quad-Core AMP Simulation

This guide details how to build and run the Quad-Core Asymmetric Multi-Processing (AMP) simulation on gem5.

## Prerequisites
- gem5 built with RISC-V support (`build/RISCV/gem5.opt`)
- Zephyr SDK installed
- RISC-V GNU Toolchain (for bootloader)

## 1. Build gem5
Ensure gem5 is built with the latest changes:
```bash
cd src/gem5
scons build/RISCV/gem5.opt -j$(nproc)
cd ../..
```

## 2. Build Bootloader
Compile the custom multi-core bootloader:
```bash
riscv64-unknown-elf-gcc -march=rv32imac -mabi=ilp32 -nostdlib -Ttext 0x80000000 -o src/bootloader/bootloader.elf src/bootloader/boot.S
```

## 3. Build Zephyr Kernels
Build the "Hello World" application for each of the 4 cores. Each core has a specific memory configuration defined in its overlay.

**Core 0:**
```bash
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core0 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core0.overlay" -DCONFIG_RV_BOOT_HART=0
```

**Core 1:**
```bash
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core1 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core1.overlay" -DCONFIG_RV_BOOT_HART=1
```

**Core 2:**
```bash
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core2 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core2.overlay" -DCONFIG_RV_BOOT_HART=2
```

**Core 3:**
```bash
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core3 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core3.overlay" -DCONFIG_RV_BOOT_HART=3
```

## 4. Run Simulation
Execute the simulation using the `fs_quad_amp.py` configuration script:

```bash
src/gem5/build/RISCV/gem5.opt configs/riscv_rt/fs_quad_amp.py \
    --kernels src/zephyr_apps/hello_world/build_core0/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core1/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core2/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core3/zephyr/zephyr.elf \
    --bootloader src/bootloader/bootloader.elf
```

## 5. Verify Output
Check the terminal output for each core in the `m5out` directory:

```bash
cat m5out/system.platform.terminal   # Core 0
cat m5out/system.platform.terminal1  # Core 1
cat m5out/system.platform.terminal2  # Core 2
cat m5out/system.platform.terminal3  # Core 3
```

You should see "Hello World!" from each core.
