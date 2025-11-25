# Phase 1 Report: gem5 RISC-V RT Baseline

## Executive Summary

This report documents the completion of Phase 1 of the gem5 RISC-V Real-Time Simulation Framework project. We have successfully established a full-system simulation environment capable of running the Zephyr RTOS and executing automotive-grade real-time workloads.

**Key Achievements:**
- **Full-System Simulation**: Validated gem5 RISC-V configuration with 500MHz CPU, 128MB RAM, and hierarchical caches.
- **Zephyr RTOS Integration**: Successfully ported Zephyr v4.3.0 to a custom `gem5_riscv32` board definition.
- **Automotive Workload**: Implemented and verified a periodic control loop with 1ms hard real-time deadline.
- **Performance**: Achieved 100% deadline compliance with 0.42 IPC and minimal cache miss rates.
- **Automation**: Established a complete pipeline for simulation execution, logging, and metrics extraction.

## System Configuration

| Component | Specification | Notes |
|-----------|---------------|-------|
| **CPU** | RISC-V 32-bit (RV32IMAC) | In-order MinorCPU @ 500 MHz |
| **Memory** | 128 MB DDR3 | Base address 0x80000000 |
| **L1 I-Cache** | 32 KB, 2-way | Latency: 1 cycle |
| **L1 D-Cache** | 32 KB, 2-way | Latency: 2 cycles |
| **L2 Cache** | 256 KB, 8-way | Latency: 10 cycles |
| **OS** | Zephyr RTOS v4.3.0 | Custom `gem5_riscv32` board |
| **Workload** | Periodic Control Loop | 1ms period, PID/State Machine |

## Baseline Performance Metrics

Performance data collected from 1100 iterations of the automotive control loop workload:

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **IPC** | 0.42 | High efficiency for in-order core |
| **L1 I-Cache Miss Rate** | 0.004% | Excellent code locality |
| **L1 D-Cache Miss Rate** | 0.004% | Excellent data locality |
| **L2 Cache Miss Rate** | 98.3% | Cold start dominance (short run) |
| **Avg Response Time** | ~102 μs | 10% of 1ms deadline |
| **Deadline Compliance** | 100.0% | Hard real-time requirements met |

## Known Limitations

1. **Memory Technology**: Currently using standard DDR3. STT-MRAM models are not yet integrated (planned for Phase 2).
2. **TCM**: Tightly Coupled Memory is not configured in the baseline (planned for Phase 2).
3. **Parameter Sweeps**: No automated design space exploration yet.
4. **Peripherals**: Only UART and Timer are simulated; no complex automotive buses (CAN/LIN).

## Phase 2 Preview

The next phase will focus on "Memory Architecture Exploration":
- **STT-MRAM Integration**: Modeling non-volatile memory characteristics.
- **TCM Implementation**: Adding scratchpad memory for critical tasks.
- **Design Space Exploration**: Sweeping cache sizes and memory latencies.
- **Advanced Workloads**: More complex automotive scenarios.

## Reproduction Instructions

To reproduce these results from a clean environment:

1. **Clone Repository**:
   ```bash
   git clone https://github.com/cometzero/gem5_riscv_rt.git
   cd gem5_riscv_rt
   ```

2. **Install Dependencies**:
   ```bash
   ./scripts/install_zephyr_deps.sh
   ./scripts/install_zephyr_sdk.sh
   ```

3. **Build gem5**:
   ```bash
   ./scripts/build_gem5.sh
   ```

4. **Build Workload**:
   ```bash
   ./scripts/build_zephyr.sh gem5_riscv32 workloads/automotive/control_loop
   ```

5. **Run Simulation**:
   ```bash
   ./scripts/run_sim.sh baseline src/zephyr/build/zephyr/zephyr.elf
   ```

6. **Generate Report**:
   ```bash
   ./scripts/postprocess_baseline.py --input-dir build/results
   ```

Results will be available in `docs/results/baseline_summary.csv`.
