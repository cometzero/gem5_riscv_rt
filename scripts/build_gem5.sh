#!/bin/bash
# gem5 build script for RISC-V architecture
# Builds gem5 with RISC-V support for full-system simulation

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
BUILD_LOG="$PROJECT_ROOT/build/gem5/build.log"

echo -e "${BLUE}gem5 RISC-V Build Script${NC}"
echo "========================================"
echo ""

# Create build directory
mkdir -p "$PROJECT_ROOT/build/gem5"

# Check if gem5 submodule exists
if [ ! -d "$PROJECT_ROOT/src/gem5" ]; then
    echo -e "${RED}Error: gem5 submodule not found at src/gem5${NC}"
    echo "Run: git submodule update --init"
    exit 1
fi

# Check for build dependencies
echo -e "${YELLOW}Checking build dependencies...${NC}"
MISSING_DEPS=0

if ! command -v scons &> /dev/null; then
    echo -e "${RED}✗ scons not found${NC}"
    echo "  Install: pip3 install scons"
    MISSING_DEPS=1
fi

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ python3 not found${NC}"
    MISSING_DEPS=1
fi

if [ $MISSING_DEPS -eq 1 ]; then
    echo -e "${RED}Missing dependencies. Please install them first.${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Dependencies check passed${NC}"
echo ""

# Navigate to gem5 directory
cd "$PROJECT_ROOT/src/gem5"

# Build gem5 for RISC-V
echo -e "${YELLOW}Building gem5 for RISC-V...${NC}"
echo "This may take 1-2 hours depending on your system"
echo "Build log: $BUILD_LOG"
echo ""

# Determine build arguments
BUILD_ARGS="build/RISCV/gem5.opt -j$(nproc)"
PROTOCOL=$1

if [ -n "$PROTOCOL" ]; then
    echo "Building with Ruby Protocol: $PROTOCOL"
    BUILD_ARGS="$BUILD_ARGS PROTOCOL=$PROTOCOL"
fi

# Run scons build
scons $BUILD_ARGS 2>&1 | tee "$BUILD_LOG"

# Check build result
if [ ${PIPESTATUS[0]} -eq 0 ]; then
    echo ""
    echo -e "${GREEN}✓ gem5 build successful${NC}"
    echo "Binary: $PROJECT_ROOT/src/gem5/build/RISCV/gem5.opt"
    
    # Verify binary exists
    if [ -f "$PROJECT_ROOT/src/gem5/build/RISCV/gem5.opt" ]; then
        echo ""
        echo "gem5 version:"
        "$PROJECT_ROOT/src/gem5/build/RISCV/gem5.opt" --version
    fi
    
    exit 0
else
    echo ""
    echo -e "${RED}✗ gem5 build failed${NC}"
    echo "Check build log for errors: $BUILD_LOG"
    
    # Print last 20 lines of errors
    echo ""
    echo "Last errors from build log:"
    grep -i error "$BUILD_LOG" | tail -20 || echo "No specific errors found in log"
    
    exit 1
fi
