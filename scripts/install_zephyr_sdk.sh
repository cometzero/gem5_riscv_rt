#!/bin/bash
set -e

SDK_VERSION="0.16.5"
SDK_FILENAME="zephyr-sdk-${SDK_VERSION}_linux-x86_64.tar.xz"
SDK_URL="https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v${SDK_VERSION}/${SDK_FILENAME}"
INSTALL_DIR="$HOME/zephyr-sdk-${SDK_VERSION}"

echo "Checking for Zephyr SDK at $INSTALL_DIR..."

if [ ! -d "$INSTALL_DIR" ]; then
    echo "Downloading Zephyr SDK ${SDK_VERSION}..."
    wget -c "$SDK_URL"
    
    echo "Extracting Zephyr SDK..."
    tar xf "$SDK_FILENAME" -C "$HOME"
    rm "$SDK_FILENAME"
    
    echo "Running SDK setup..."
    # Install all toolchains (-a) or just riscv64 (-t riscv64-zephyr-elf)
    # We use -t riscv64-zephyr-elf to save space/time, it supports both 32 and 64 bit
    "$INSTALL_DIR/setup.sh" -t riscv64-zephyr-elf -h -c
else
    echo "Zephyr SDK already installed."
fi

echo "Zephyr SDK setup complete."
