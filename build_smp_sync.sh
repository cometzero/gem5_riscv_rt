#!/bin/bash
set -e

APP_DIR="src/zephyr_apps/smp_synchronization"
ZEPHYR_BASE="src/zephyr/zephyr"
BOARD_DIR="boards/riscv/gem5_octa"

# Backup original hifive1.dts
HIFIVE_DTS="${ZEPHYR_BASE}/boards/sifive/hifive1/hifive1.dts"
cp ${HIFIVE_DTS} ${HIFIVE_DTS}.bak

# Overwrite with gem5_octa.dts (workaround for board discovery)
cp ${APP_DIR}/${BOARD_DIR}/gem5_octa.dts ${HIFIVE_DTS}

export ZEPHYR_BASE=$(pwd)/${ZEPHYR_BASE}
cd ${APP_DIR}

echo "Building SMP Synchronization App..."
west build -b hifive1 -d build_smp_sync --pristine
echo "Build complete."

# Restore original hifive1.dts
cp ${HIFIVE_DTS}.bak ${HIFIVE_DTS}
rm ${HIFIVE_DTS}.bak
echo "hifive1.dts restored."
