#!/bin/bash
set -e

# Paths
APP_DIR="src/zephyr_apps/smp_hello"
ZEPHYR_BASE="src/zephyr/zephyr"
HIFIVE_DTS="${ZEPHYR_BASE}/boards/sifive/hifive1/hifive1.dts"
GEM5_OCTA_DTS="${APP_DIR}/boards/riscv/gem5_octa/gem5_octa.dts"

# Backup original hifive1.dts
if [ ! -f "${HIFIVE_DTS}.bak" ]; then
    cp "${HIFIVE_DTS}" "${HIFIVE_DTS}.bak"
fi

# Overwrite with gem5_octa.dts
cp "${GEM5_OCTA_DTS}" "${HIFIVE_DTS}"

# Build
export ZEPHYR_BASE=$(pwd)/${ZEPHYR_BASE}
cd ${APP_DIR}
west build -b hifive1 -d build_smp --pristine

# Restore original hifive1.dts
cd ../../..
cp "${HIFIVE_DTS}.bak" "${HIFIVE_DTS}"

echo "Build complete. hifive1.dts restored."
