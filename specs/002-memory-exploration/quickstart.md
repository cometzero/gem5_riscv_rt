# Quickstart: Phase 2 Memory Exploration

## Prerequisites

- gem5 built with Ruby support:
  ```bash
  scons build/RISCV/gem5.opt PROTOCOL=MI_example
  ```
- Zephyr SDK installed.

## Running a Mixed-Memory Simulation

1. **Build Zephyr with SRAM config**:
   ```bash
   ./scripts/build_zephyr.sh gem5_riscv32_sram workloads/automotive/mixed_criticality
   ```

2. **Run Simulation (SRAM Boot + DRAM)**:
   ```bash
   ./scripts/run_sim.sh sram_boot src/zephyr/build/zephyr/zephyr.elf --mem-type=dram
   ```

3. **Run Simulation (STT-MRAM)**:
   ```bash
   ./scripts/run_sim.sh sram_boot src/zephyr/build/zephyr/zephyr.elf --mem-type=mram
   ```

4. **Analyze Results**:
   ```bash
   ./scripts/postprocess_dse.py --input-dir build/results
   ```
