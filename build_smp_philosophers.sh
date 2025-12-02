#!/bin/bash
set -e

# Paths
APP_DIR="src/zephyr_apps/smp_philosophers"
ZEPHYR_BASE="src/zephyr/zephyr"
HIFIVE_DTS="${ZEPHYR_BASE}/boards/sifive/hifive1/hifive1.dts"
GEM5_OCTA_DTS="${APP_DIR}/gem5_smp.overlay" 
# Note: The overlay logic in build_smp.sh was replacing the DTS. 
# But here we have an overlay. 
# If build_smp.sh was replacing the DTS with a full DTS, that's one thing.
# But gem5_smp.overlay suggests it's an overlay.
# Let's check build_smp.sh again. It says GEM5_OCTA_DTS="${APP_DIR}/boards/riscv/gem5_octa/gem5_octa.dts"
# But I copied gem5_smp.overlay.
# I should check if smp_hello has a full DTS or just an overlay.
# If it's an overlay, I should use it as an overlay.
# But build_smp.sh was overwriting the board DTS.
# Let's stick to what build_smp.sh did if I can.
# Wait, build_smp.sh used `boards/riscv/gem5_octa/gem5_octa.dts`.
# I don't have that in smp_philosophers.
# I copied `gem5_smp.overlay`.
# Maybe I should use the overlay with west build -DTC_OVERLAY_FILE=...
# Let's try to build with overlay first, it's cleaner.

export ZEPHYR_BASE=$(pwd)/${ZEPHYR_BASE}
cd ${APP_DIR}

# Clean build
rm -rf build_smp

# Build with overlay
west build -b hifive1 -d build_smp -- -DDTC_OVERLAY_FILE=gem5_smp.overlay

echo "Build complete."
