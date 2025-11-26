# Phase 2 Memory Exploration Walkthrough

## Overview
This document details the verification steps for Phase 2, focusing on SRAM boot functionality with both Classic and Ruby memory systems.

## Verification Steps

### T010: Verify SRAM Boot (Classic)

**Goal:** Ensure Zephyr boots from SRAM using the Classic Memory system.

### Phase 4: Zephyr OS Integration
- **Goal**: Boot Zephyr OS on the gem5 RISC-V platform.
- **Status**: Completed.
- **Verification**:
  - Successfully built Zephyr `philosophers` sample for `gem5_riscv` board.
  - Ran simulation with `--kernel` pointing to `zephyr.elf`.
  - Verified console output showing Zephyr boot banner and thread execution.
  - Confirmed `uart` output is correctly routed to `system.platform.terminal`.

### Phase 5: STT-MRAM Implementation
- **Goal**: Implement STT-MRAM memory controller with asymmetric read/write latencies.
- **Status**: Completed.
- **Implementation Details**:
  - Created `STTMRAM` class inheriting from `NVMInterface`.
  - Configured asymmetric latencies: `tREAD=20ns`, `tWRITE=100ns`.
  - Implemented memory controller replacement logic in `configs/riscv_rt/ruby/system.py` to swap the default DRAM controller with STT-MRAM at runtime.
  - Resolved `clk_domain` and parenting issues by disabling the default controller and explicitly parenting the new `STTMRAM` controller.
- **Verification**:
  - Ran simulation with `--mem-tech=mram`.
  - Verified `config.ini` shows `system.mram_ctrl` with `type=NVMInterface` and correct timing parameters (`tREAD=20000`, `tWRITE=100000`).
  - Analyzed `stats.txt` confirming `system.mram_ctrl` activity (`readBursts=14`, `avgMemAccLat` ~16.8ns).
  - Confirmed simulation runs successfully for 20M ticks.

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
