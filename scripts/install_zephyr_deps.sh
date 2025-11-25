#!/bin/bash
set -e

echo "Installing Zephyr system dependencies..."
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
    git cmake ninja-build gperf \
    ccache dfu-util device-tree-compiler wget \
    python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file \
    make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1 python3-venv

echo "Setting up virtual environment..."
if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

echo "Installing west..."
pip install -U pip
pip install -U west

echo "Verifying west installation..."
west --version

echo "Dependencies installed successfully. Activate venv with: source .venv/bin/activate"
