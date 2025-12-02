#!/bin/bash
set -e

APP_DIR="src/zephyr_apps/hello_world"
ZEPHYR_BASE="src/zephyr/zephyr"

export ZEPHYR_BASE=$(pwd)/${ZEPHYR_BASE}
cd ${APP_DIR}

for i in {0..3}
do
    echo "CONFIG_RV_BOOT_HART=${i}" > gem5_amp_core${i}.conf
    echo "Building AMP Kernel for Core ${i}..."
    west build -b hifive1 -d build_core${i} --pristine -- \
        -DEXTRA_CONF_FILE="gem5_amp.conf;gem5_amp_core${i}.conf" \
        -DEXTRA_DTC_OVERLAY_FILE=gem5_amp_core${i}.overlay
    rm gem5_amp_core${i}.conf
    echo "Core ${i} build complete."
done

echo "All AMP kernels built successfully."
