# Phase 2 Report: Memory Architecture Exploration

## Executive Summary

Phase 2 of the gem5 RISC-V Real-Time Simulation Framework project focused on "Memory Architecture Exploration". We successfully extended the simulation environment to support a heterogeneous memory hierarchy consisting of Boot ROM, NOR Flash, SRAM, and Main Memory (DRAM or STT-MRAM). This enables the execution of mixed-criticality workloads where critical tasks run in fast, deterministic SRAM while background tasks utilize larger, slower main memory.

**Key Achievements:**
- **Heterogeneous Memory Map**: Implemented a realistic memory map with distinct regions for ROM (0x0), Flash (0x20M), SRAM (0x80M), and Main Memory (0x80.2M).
- **SRAM Boot Support**: Validated Zephyr RTOS booting directly from SRAM, bypassing the need for DRAM initialization for critical startup.
- **STT-MRAM Modeling**: Integrated an STT-MRAM model with asymmetric read/write latency characteristics into the gem5 memory system.
- **Ruby Memory Integration**: Configured the Ruby `MI_example` protocol to support disjoint memory ranges, enabling more accurate cache coherence modeling for real-time systems.

## System Configuration

The updated system configuration features a complex memory hierarchy designed for automotive real-time applications.

| Component | Address Range | Size | Type | Usage |
|-----------|---------------|------|------|-------|
| **Boot ROM** | `0x00000000` | 64 KB | ROM | Reset vector, Bootloader |
| **NOR Flash** | `0x20000000` | 32 MB | SimpleMemory | XIP Code, Storage |
| **SRAM** | `0x80000000` | 2 MB | SimpleMemory | **Critical** Code/Data (0-wait state ideal) |
| **Main Memory** | `0x80200000` | 126 MB | DRAM / MRAM | Background Tasks, Heap |

### STT-MRAM Configuration
The STT-MRAM model is configured as a drop-in replacement for DRAM in the Main Memory region, with the following timing characteristics (modeled):
- **Read Latency**: ~20ns (Comparable to DRAM)
- **Write Latency**: ~100ns (5x slower than DRAM)
- **Persistence**: Non-volatile (retains data without power)

## Experiment Results

We conducted regression tests to validate the memory hierarchy and compare the performance of DRAM vs. STT-MRAM configurations.

### 1. Latency Analysis (Short Regression)
*Simulation Duration: 20 μs (20M ticks)*

| Memory Type | Region | Avg Access Latency (Tick) | Notes |
|-------------|--------|---------------------------|-------|
| **SRAM** | `0x80000000` | ~22,187 | Consistent across configurations |
| **DRAM** | `0x80200000` | ~21,923 | Standard DDR3 model |
| **STT-MRAM** | `0x80200000` | N/A | No accesses observed in short run |

**Observation**:
- The SRAM and DRAM latencies are observed to be similar (~22ns) in the current Ruby `MI_example` configuration. This suggests that the interconnect (NoC) or cache controller overhead dominates the raw device latency in this specific configuration.
- In the short 20μs regression test, the workload primarily executed from SRAM (as intended for critical tasks), resulting in no significant accesses to the Main Memory (MRAM) region. Longer simulations are required to fully characterize the impact of MRAM's asymmetric latencies on background tasks.

### 2. Mixed Criticality Workload
The system successfully executed a mixed-criticality workload where:
- **Critical Task**: Mapped to `.sram_text` and `.sram_data`, executing from SRAM.
- **Background Task**: Mapped to standard memory, residing in DRAM/MRAM.

Verification confirmed that the CPU correctly fetches instructions from the 0x80000000 (SRAM) range during the critical loop execution.

## Known Limitations & Future Work

1. **MRAM Access in Short Tests**: The current regression tests are too short to trigger significant background task activity in Main Memory. Future experiments should run for >100ms to validate MRAM performance impact.
2. **Ruby Latency Overhead**: The observed latency for SRAM (~22ns) is higher than the ideal 1-2ns hardware target. This is likely due to the default topology and router latency in the Ruby network. Optimizing the Ruby config for a "direct connect" or low-latency bus is a Phase 3 target.
3. **DSE Automation**: While the scripts support parameter sweeps, fully automated Design Space Exploration (DSE) with visualization is pending.

## Conclusion

Phase 2 has successfully established the structural foundation for memory architecture exploration. The platform can now model heterogeneous memory types and execute spatially isolated mixed-criticality workloads. While fine-tuning of latency models and longer simulation runs are needed for detailed performance characterization, the core capabilities are functional and ready for advanced research.
