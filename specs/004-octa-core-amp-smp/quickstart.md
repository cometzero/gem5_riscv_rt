# Quickstart: Octa-Core AMP/SMP Simulation

This guide details how to build and run the Octa-Core Hybrid AMP/SMP simulation on gem5.

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

### Cluster 0 (AMP)
Build independent kernels for Cores 0-3:
```bash
# Core 0
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core0 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core0.overlay" -DCONFIG_RV_BOOT_HART=0

# Core 1
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core1 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core1.overlay" -DCONFIG_RV_BOOT_HART=1

# Core 2
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core2 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core2.overlay" -DCONFIG_RV_BOOT_HART=2

# Core 3
west build -p always -b hifive1 -d src/zephyr_apps/hello_world/build_core3 src/zephyr_apps/hello_world -- -DDTC_OVERLAY_FILE="gem5_amp_core3.overlay" -DCONFIG_RV_BOOT_HART=3
```

### Cluster 1 (SMP)
Build a single SMP kernel for Cores 4-7:
```bash
# SMP Kernel (Primary Core 4)
west build -p always -b hifive1 -d src/zephyr_apps/smp_hello/build_smp src/zephyr_apps/smp_hello -- -DDTC_OVERLAY_FILE="gem5_smp.overlay" -DCONFIG_RV_BOOT_HART=4
```

## 4. Run Simulation
Execute the simulation using the `fs_octa_hybrid.py` configuration script:

```bash
src/gem5/build/RISCV/gem5.opt configs/riscv_rt/fs_octa_hybrid.py \
    --kernels src/zephyr_apps/hello_world/build_core0/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core1/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core2/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core3/zephyr/zephyr.elf,src/zephyr_apps/smp_hello/build_smp/zephyr/zephyr.elf \
    --bootloader src/bootloader/bootloader.elf
```

## 5. Verify Output
Check the terminal output for each context:

```bash
cat m5out/system.platform.terminal   # Core 0 (AMP)
cat m5out/system.platform.terminal1  # Core 1 (AMP)
cat m5out/system.platform.terminal2  # Core 2 (AMP)
cat m5out/system.platform.terminal3  # Core 3 (AMP)
cat m5out/system.platform.terminal4  # Cluster 1 (SMP Shared)
```
