cmake_minimum_required(VERSION 3.20.0)
find_package(Zephyr REQUIRED HINTS $ENV{ZEPHYR_BASE})
project(mixed_criticality)

target_sources(app PRIVATE src/main.c src/critical.c src/background.c)

# Relocate background.c to RAM (DRAM)
# Default code placement is in FLASH (SRAM) due to zephyr,flash = &ram0
# We move non-critical code to RAM (DRAM)
zephyr_code_relocate(FILES src/background.c LOCATION RAM)
