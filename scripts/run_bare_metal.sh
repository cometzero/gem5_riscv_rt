#!/bin/bash
# Run bare-metal program on gem5 RISC-V full-system simulation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

GEM5_BIN="$PROJECT_ROOT/src/gem5/build/RISCV/gem5.opt"
CONFIG="$PROJECT_ROOT/configs/riscv_rt/base_fs.py"
KERNEL="$PROJECT_ROOT/workloads/bare_metal/hello.elf"

# Check if gem5 binary exists
if [ ! -f "$GEM5_BIN" ]; then
    echo "Error: gem5 binary not found at $GEM5_BIN"
    echo "Run: ./scripts/build_gem5.sh"
    exit 1
fi

# Check if kernel exists
if [ ! -f "$KERNEL" ]; then
    echo "Error: Kernel not found at $KERNEL"
    echo "Run: cd workloads/bare_metal && make"
    exit 1
fi

echo "Running gem5 RISC-V full-system simulation"
echo "==========================================="
echo "gem5:   $GEM5_BIN"
echo "Config: $CONFIG"
echo "Kernel: $KERNEL"
echo ""

# Run simulation
"$GEM5_BIN" "$CONFIG" --kernel="$KERNEL"
