#!/bin/bash
# Script to run gem5 simulation with specified configuration and workload
# Usage: ./scripts/run_sim.sh <CONFIG_NAME> <WORKLOAD_PATH> [MAX_TICKS]

set -e

# Arguments
CONFIG_NAME=$1
WORKLOAD_PATH=$2
MAX_TICKS=${3:-1000000000000}  # Default: 1 trillion ticks (2s @ 500MHz)

if [ -z "$CONFIG_NAME" ] || [ -z "$WORKLOAD_PATH" ]; then
    echo "Usage: $0 <CONFIG_NAME> <WORKLOAD_PATH> [MAX_TICKS]"
    echo "Example: $0 baseline src/zephyr/build/zephyr/zephyr.elf"
    exit 1
fi

# Paths
PROJECT_ROOT=$(pwd)
GEM5_BIN="$PROJECT_ROOT/src/gem5/build/RISCV/gem5.opt"
CONFIG_SCRIPT="$PROJECT_ROOT/configs/riscv_rt/base_fs.py"
OUTPUT_DIR="$PROJECT_ROOT/build/results/$CONFIG_NAME/$(basename $WORKLOAD_PATH .elf)"

# Check if gem5 binary exists
if [ ! -f "$GEM5_BIN" ]; then
    echo "Error: gem5 binary not found at $GEM5_BIN"
    echo "Please build gem5 first: ./scripts/build_gem5.sh"
    exit 1
fi

# Check if workload exists
if [ ! -f "$WORKLOAD_PATH" ]; then
    echo "Error: Workload not found at $WORKLOAD_PATH"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "Output directory created: $OUTPUT_DIR"

echo "Starting simulation..."
echo "Configuration: $CONFIG_NAME"
echo "Workload: $WORKLOAD_PATH"
echo "Max Ticks: $MAX_TICKS"
echo "Log file: $OUTPUT_DIR/sim.log"

# Run gem5
$GEM5_BIN -d "$OUTPUT_DIR" "$CONFIG_SCRIPT" \
    --kernel="$WORKLOAD_PATH" \
    --max-ticks="$MAX_TICKS" \
    2>&1 | tee "$OUTPUT_DIR/sim.log"

EXIT_CODE=${PIPESTATUS[0]}

if [ $EXIT_CODE -eq 0 ]; then
    echo ""
    echo "Simulation completed successfully."
    echo "Results saved to $OUTPUT_DIR"
else
    echo ""
    echo "Simulation failed with exit code $EXIT_CODE"
    exit $EXIT_CODE
fi
