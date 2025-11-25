#!/bin/bash
# Script to run Zephyr RTOS on gem5
# Usage: ./scripts/run_zephyr.sh

set -e

# Paths
GEM5_BIN=src/gem5/build/RISCV/gem5.opt
CONFIG_SCRIPT=configs/riscv_rt/base_fs.py
KERNEL=src/zephyr/build/zephyr/zephyr.elf
OUTPUT_DIR=m5out

# Check if gem5 binary exists
if [ ! -f "$GEM5_BIN" ]; then
    echo "Error: gem5 binary not found at $GEM5_BIN"
    echo "Please build gem5 first: ./scripts/build_gem5.sh"
    exit 1
fi

# Check if Zephyr kernel exists
if [ ! -f "$KERNEL" ]; then
    echo "Error: Zephyr kernel not found at $KERNEL"
    echo "Please build Zephyr first: ./scripts/build_zephyr.sh gem5_riscv32 zephyr/samples/hello_world"
    exit 1
fi

echo "Running Zephyr on gem5..."
echo "Kernel: $KERNEL"
echo "Output: $OUTPUT_DIR"

# Run gem5 with Zephyr kernel
$GEM5_BIN $CONFIG_SCRIPT --kernel=$KERNEL

echo ""
echo "Simulation complete. Check $OUTPUT_DIR/ for results."
