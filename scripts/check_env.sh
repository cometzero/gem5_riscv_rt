#!/bin/bash
# Environment check script for gem5 RISC-V Full-System Simulation
# Verifies all required tools are installed

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "Checking gem5_riscv_rt development environment..."
echo ""

ERRORS=0

# Check Python 3.11+
echo -n "Checking Python version... "
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version | awk '{print $2}')
    PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
    PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)
    
    if [ "$PYTHON_MAJOR" -ge 3 ] && [ "$PYTHON_MINOR" -ge 11 ]; then
        echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION"
    else
        echo -e "${RED}✗${NC} Python $PYTHON_VERSION (need >= 3.11)"
        ERRORS=$((ERRORS+1))
    fi
else
    echo -e "${RED}✗${NC} python3 not found"
    ERRORS=$((ERRORS+1))
fi

# Check RISC-V toolchain
echo -n "Checking RISC-V toolchain... "
if command -v riscv32-unknown-elf-gcc &> /dev/null; then
    GCC_VERSION=$(riscv32-unknown-elf-gcc --version | head -n1)
    echo -e "${GREEN}✓${NC} $GCC_VERSION"
else
    echo -e "${RED}✗${NC} riscv32-unknown-elf-gcc not found"
    echo -e "  ${YELLOW}Install from: https://github.com/riscv-collab/riscv-gnu-toolchain${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check cmake
echo -n "Checking cmake... "
if command -v cmake &> /dev/null; then
    CMAKE_VERSION=$(cmake --version | head -n1 | awk '{print $3}')
    echo -e "${GREEN}✓${NC} cmake $CMAKE_VERSION"
else
    echo -e "${RED}✗${NC} cmake not found"
    echo -e "  ${YELLOW}Install: sudo apt install cmake${NC}"
    ERRORS=$((ERRORS+1))
fi

# Check west (Zephyr)
echo -n "Checking west... "
if command -v west &> /dev/null; then
    WEST_VERSION=$(west --version)
    echo -e "${GREEN}✓${NC} west $WEST_VERSION"
else
    echo -e "${YELLOW}⚠${NC} west not found (needed for Zephyr)"
    echo -e "  ${YELLOW}Install: pip3 install west${NC}"
fi

# Check git
echo -n "Checking git... "
if command -v git &> /dev/null; then
    GIT_VERSION=$(git --version | awk '{print $3}')
    echo -e "${GREEN}✓${NC} git $GIT_VERSION"
else
    echo -e "${RED}✗${NC} git not found"
    ERRORS=$((ERRORS+1))
fi

# Check scons (gem5)
echo -n "Checking scons... "
if command -v scons &> /dev/null; then
    SCONS_VERSION=$(scons --version | head -n2 | tail -n1 | awk '{print $2}')
    echo -e "${GREEN}✓${NC} scons $SCONS_VERSION"
else
    echo -e "${YELLOW}⚠${NC} scons not found (needed for gem5)"
    echo -e "  ${YELLOW}Install: pip3 install scons${NC}"
fi

echo ""
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ All required tools are installed${NC}"
    exit 0
else
    echo -e "${RED}✗ $ERRORS error(s) found${NC}"
    echo "Please install missing tools before continuing"
    exit 1
fi
