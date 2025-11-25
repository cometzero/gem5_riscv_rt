#!/bin/bash
# Script to run automotive control loop workload on gem5
# Usage: ./scripts/run_automotive.sh

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

# Check if kernel exists
if [ ! -f "$KERNEL" ]; then
    echo "Error: Kernel not found at $KERNEL"
    echo "Please build automotive workload first:"
    echo "  ./scripts/build_zephyr.sh gem5_riscv32 ../../workloads/automotive/control_loop"
    exit 1
fi

echo "Running automotive control loop on gem5..."
echo "Kernel: $KERNEL"
echo "Output: $OUTPUT_DIR"
echo "Expected runtime: ~2-3 seconds simulated time for 1100 iterations"
echo ""

# Run gem5 with automotive workload
# Max ticks set to allow ~2 seconds of simulated time
$GEM5_BIN $CONFIG_SCRIPT --kernel=$KERNEL --max-ticks=1000000000000

echo ""
echo "Simulation complete. Check $OUTPUT_DIR/ for results."
echo "Terminal output: $OUTPUT_DIR/system.platform.terminal"
