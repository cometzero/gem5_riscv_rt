#!/bin/bash
# Create swap space to prevent OOM during gem5 compilation
# This is especially helpful for systems with limited RAM (8GB or less)

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SWAP_SIZE_GB=${1:-4}  # Default 4GB swap
SWAP_FILE="/swapfile"

echo -e "${BLUE}Swap Space Setup${NC}"
echo "=================="
echo ""

# Check if swap already exists
if swapon --show | grep -q "$SWAP_FILE"; then
    echo -e "${YELLOW}Swap file already exists and is active${NC}"
    swapon --show
    exit 0
fi

# Check if swap file exists but not active
if [ -f "$SWAP_FILE" ]; then
    echo -e "${YELLOW}Swap file exists but not active. Activating...${NC}"
    sudo swapon "$SWAP_FILE"
    echo -e "${GREEN}✓ Swap activated${NC}"
    swapon --show
    exit 0
fi

# Create new swap file
echo -e "${YELLOW}Creating ${SWAP_SIZE_GB}GB swap file...${NC}"
echo "This may take a few minutes..."

# Allocate swap file
sudo fallocate -l ${SWAP_SIZE_GB}G "$SWAP_FILE"

# Set permissions
sudo chmod 600 "$SWAP_FILE"

# Make swap
sudo mkswap "$SWAP_FILE"

# Enable swap
sudo swapon "$SWAP_FILE"

# Verify
echo ""
echo -e "${GREEN}✓ Swap space created and activated${NC}"
swapon --show

# Make it permanent (optional)
echo ""
echo -e "${YELLOW}To make swap permanent across reboots, add this line to /etc/fstab:${NC}"
echo "$SWAP_FILE none swap sw 0 0"
echo ""
echo "Run this command to add it automatically:"
echo "  echo '$SWAP_FILE none swap sw 0 0' | sudo tee -a /etc/fstab"
