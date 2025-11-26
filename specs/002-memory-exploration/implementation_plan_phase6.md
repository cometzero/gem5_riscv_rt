# Phase 6: Experiment & Polish

## Goal
Run comparative experiments between the baseline DRAM configuration and the newly implemented STT-MRAM configuration to quantify performance differences and validate the STT-MRAM model. Finalize project documentation.

## User Review Required
None. This phase focuses on experimentation and documentation.

## Proposed Changes

### Experiments
1.  **Run DRAM Baseline**:
    -   Command: `./scripts/run_sim.sh dram_test src/zephyr/build/zephyr/zephyr.elf 20000000 --boot-mode=sram --mem-tech=dram --mem-system=ruby --cpu-type=TimingSimpleCPU`
    -   Output: `build/results/dram_test/zephyr`

2.  **Run STT-MRAM Experiment** (Already done, but can re-run for consistency if needed):
    -   Command: `./scripts/run_sim.sh mram_test src/zephyr/build/zephyr/zephyr.elf 20000000 --boot-mode=sram --mem-tech=mram --mem-system=ruby --cpu-type=TimingSimpleCPU`
    -   Output: `build/results/mram_test/zephyr`

### Analysis
-   Compare `stats.txt` from both runs.
-   Key Metrics:
    -   `simSeconds`: Total simulated time (should be same if fixed ticks, but maybe different if workload finished early? No, fixed ticks).
    -   `system.mram_ctrl.dram.avgMemAccLat` vs `system.mem_ctrl.dram.avgMemAccLat`.
    -   `hostSeconds`: Simulation performance.
    -   `system.ruby.l2_cntrl0.L2cache.m_demand_misses`: Impact on cache?

### Documentation
-   Update `walkthrough.md`:
    -   Add "Phase 6: Experiment Results" section.
    -   Include a comparison table.
    -   Add screenshots or log snippets if relevant.
-   Update `tasks.md`:
    -   Mark Phase 6 tasks as complete.

## Verification Plan
-   **Automated Tests**: None (experiments are the test).
-   **Manual Verification**: Review `stats.txt` and `walkthrough.md`.
