#!/bin/bash
# Install optional gem5 dependencies for better performance and features
# These are not required but recommended for optimal gem5 experience

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}gem5 Optional Dependencies Installer${NC}"
echo "========================================"
echo ""
echo "This script will install optional dependencies that:"
echo "  • Improve build performance (tcmalloc)"
echo "  • Enable tracing support (protobuf)"
echo "  • Enable PNG framebuffer support (libpng)"
echo "  • Enable HDF5 support (libhdf5)"
echo "  • Enable disassembly support (capstone)"
echo ""

# Detect package manager
if command -v apt-get &> /dev/null; then
    PKG_MGR="apt-get"
    INSTALL_CMD="sudo apt-get install -y"
elif command -v yum &> /dev/null; then
    PKG_MGR="yum"
    INSTALL_CMD="sudo yum install -y"
else
    echo -e "${RED}Error: No supported package manager found (apt-get or yum)${NC}"
    exit 1
fi

echo -e "${YELLOW}Using package manager: $PKG_MGR${NC}"
echo ""

# Update package list
echo -e "${YELLOW}Updating package list...${NC}"
if [ "$PKG_MGR" = "apt-get" ]; then
    sudo apt-get update
fi

# Install dependencies
echo ""
echo -e "${YELLOW}Installing dependencies...${NC}"

if [ "$PKG_MGR" = "apt-get" ]; then
    $INSTALL_CMD \
        libgoogle-perftools-dev \
        protobuf-compiler \
        libprotobuf-dev \
        libpng-dev \
        libhdf5-dev \
        libcapstone-dev
else
    # RedHat/CentOS packages
    $INSTALL_CMD \
        gperftools-devel \
        protobuf-compiler \
        protobuf-devel \
        libpng-devel \
        hdf5-devel \
        capstone-devel
fi

echo ""
echo -e "${GREEN}✓ All optional dependencies installed successfully${NC}"
echo ""
echo "You can now rebuild gem5 to take advantage of these features:"
echo "  ./scripts/build_gem5.sh"
