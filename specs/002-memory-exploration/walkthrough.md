# Phase 2 Memory Exploration Walkthrough

## Overview
This document details the verification steps for Phase 2, focusing on SRAM boot functionality with both Classic and Ruby memory systems.

## Verification Steps

### T010: Verify SRAM Boot (Classic)

**Goal:** Ensure Zephyr boots from SRAM using the Classic Memory system.

**Command:**
```bash
./scripts/run_sim.sh sram_boot_classic src/zephyr/build/zephyr/zephyr.elf 1000000000 --boot-mode=sram --mem-system=classic
```

**Results:**
- Simulation completed successfully.
- Terminal output confirmed Zephyr boot and "Automotive Control Loop" application start.
- Log file: `build/results/sram_boot_classic/zephyr/sim.log`

### T011: Verify SRAM Boot (Ruby)

**Goal:** Ensure Zephyr boots from SRAM using the Ruby Memory system (MI_example protocol).

**Command:**
```bash
./scripts/run_sim.sh sram_boot_ruby src/zephyr/build/zephyr/zephyr.elf 1000000000 --boot-mode=sram --mem-system=ruby --cpu-type=TimingSimpleCPU
```

**Results:**
- Simulation completed successfully.
- Terminal output confirmed Zephyr boot.
- Log file: `build/results/sram_boot_ruby/zephyr/sim.log`
- **Note:** Required using `TimingSimpleCPU` instead of `MinorCPU` for Ruby compatibility/stability in this configuration.

## Key Configuration Changes

- **Zephyr Board:** Created `boards/gem5/riscv32_sram` with heterogeneous memory map (SRAM, Flash, DRAM).
- **gem5 Config:** Refactored `base_fs.py` to support `--mem-system` switch and properly wire IO/DMA ports for Ruby.
- **Ruby System:** Implemented `configs/riscv_rt/ruby/system.py` to configure `MI_example` protocol and connect to system IO.

## Next Steps
- Proceed to Phase 4: Mixed Workloads (Critical code in SRAM, non-critical in DRAM).

### T016: Verify Mixed Workload Execution

**Goal:** Verify that critical code runs from SRAM and background code runs from DRAM.

**Workload:** `workloads/automotive/mixed_criticality`
- `critical_task`: Placed in SRAM (via XIP/Flash region).
- `background_task`: Relocated to DRAM (via `zephyr_code_relocate`).

**Command (Classic):**
```bash
./scripts/run_sim.sh mixed_classic src/zephyr/build/zephyr/zephyr.elf 1000000000 --boot-mode=sram --mem-system=classic
```

**Command (Ruby):**
```bash
./scripts/run_sim.sh mixed_ruby src/zephyr/build/zephyr/zephyr.elf 1000000000 --boot-mode=sram --mem-system=ruby --cpu-type=TimingSimpleCPU
```

**Results:**
- Both simulations completed successfully.
- Terminal output confirmed execution of both tasks:
  ```
  Critical Task: 0 (SRAM)
  Background Task: 0 (DRAM)
  ```
- `readelf` confirmed symbol placement:
  - `critical_task` @ `0x8000xxxx` (SRAM)
  - `background_task` @ `0x8020xxxx` (DRAM)

## Next Steps
- Proceed to Phase 5: STT-MRAM (Implement NVM interface and Ruby parameters).
