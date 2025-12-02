#!/bin/bash
set -e

GEM5_BIN="src/gem5/build/RISCV/gem5.opt"
CONFIG_SCRIPT="configs/riscv_rt/fs_octa_hybrid.py"
BOOTLOADER="src/bootloader/bootloader.elf"

# AMP Kernels
AMP_K0="src/zephyr_apps/hello_world/build_core0/zephyr/zephyr.elf"
AMP_K1="src/zephyr_apps/hello_world/build_core1/zephyr/zephyr.elf"
AMP_K2="src/zephyr_apps/hello_world/build_core2/zephyr/zephyr.elf"
AMP_K3="src/zephyr_apps/hello_world/build_core3/zephyr/zephyr.elf"

# SMP Kernel (Synchronization App)
SMP_K="src/zephyr_apps/smp_synchronization/build_smp_sync/zephyr/zephyr.elf"

KERNELS="${AMP_K0},${AMP_K1},${AMP_K2},${AMP_K3},${SMP_K}"

echo "Starting Octa-Core Simulation with SMP Synchronization Workload..."
${GEM5_BIN} ${CONFIG_SCRIPT} --kernels ${KERNELS} --bootloader ${BOOTLOADER}
