#!/bin/bash
set -e

echo "Building Bootloader..."
cd src/bootloader
make clean
make
echo "Bootloader build complete: src/bootloader/bootloader.elf"
