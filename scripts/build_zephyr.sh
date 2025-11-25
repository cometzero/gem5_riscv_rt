#!/bin/bash
# Script to build Zephyr RTOS
# Usage: ./scripts/build_zephyr.sh [BOARD] [APP_DIR]

set -e

# Default values
BOARD=${1:-qemu_riscv32}
APP_DIR=${2:-samples/hello_world}
BUILD_DIR=build/zephyr

# Create build directory for logs
mkdir -p $BUILD_DIR

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Set Zephyr SDK path
export ZEPHYR_SDK_INSTALL_DIR=$HOME/zephyr-sdk-0.16.8

echo "Building Zephyr for board: $BOARD, app: $APP_DIR"
echo "Log file: $BUILD_DIR/build.log"

# Go to Zephyr workspace root
cd src/zephyr

# Check if board is custom and set BOARD_DIR
BOARD_PATH="$(pwd)/../../boards/riscv/$BOARD"
EXTRA_ARGS=""
if [ -d "$BOARD_PATH" ]; then
    echo "Using custom board dir: $BOARD_PATH"
    EXTRA_ARGS="-DBOARD_DIR=$BOARD_PATH"
fi

# Build using west
# 2>&1 | tee ... captures both stdout and stderr
# Add project root to BOARD_ROOT to find custom boards
west build -b $BOARD $APP_DIR -- -DBOARD_ROOT=$(pwd)/../../ $EXTRA_ARGS 2>&1 | tee ../../$BUILD_DIR/build.log

# Check for errors in the log (redundant with set -e but good for explicit check if pipe hides exit code)
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo "✓ Zephyr build successful"
else
    echo "✗ Zephyr build failed"
    exit 1
fi
