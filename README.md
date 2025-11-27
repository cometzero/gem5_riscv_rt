# gem5 RISC-V Real-Time Simulation Framework

This project provides a full-system simulation environment for RISC-V Real-Time Systems using **gem5** and **Zephyr RTOS**. It is designed to enable research into computer architecture for automotive and mixed-criticality applications, with a focus on memory hierarchy exploration (SRAM, DRAM, STT-MRAM).

## Project Overview

The framework allows for the simulation of complex real-time workloads on a customizable RISC-V SoC. It supports:
- **Full-System Simulation**: Booting Zephyr RTOS on a modeled RISC-V 32-bit processor.
- **Heterogeneous Memory**: Modeling Boot ROM, NOR Flash, On-Chip SRAM, and Main Memory (DRAM/STT-MRAM).
- **Mixed-Criticality Workloads**: Running critical real-time tasks in isolated SRAM regions while background tasks use main memory.
- **Design Space Exploration**: Analyzing the impact of memory technologies (e.g., STT-MRAM latency) on real-time performance.

## Phases & Features

### Phase 1: Baseline System
*Status: Complete*
- **Core**: RISC-V 32-bit (RV32IMAC) MinorCPU @ 500 MHz.
- **OS**: Zephyr RTOS v4.3.0 ported to a custom `gem5_riscv32` board.
- **Workload**: Periodic automotive control loop with 1ms hard real-time deadline.
- **Result**: Validated baseline performance with 100% deadline compliance.
- [View Phase 1 Report](docs/phase1_report.md)

### Phase 2: Memory Architecture Exploration
*Status: Complete*
- **Memory Map**: Added support for Boot ROM (0x0), Flash (0x20M), and SRAM (0x80M).
- **SRAM Boot**: Enabled booting Zephyr directly from SRAM for instant-on capability.
- **STT-MRAM**: Integrated a non-volatile memory model with asymmetric read/write latencies.
- **Mixed Workloads**: Implemented spatial isolation for critical vs. non-critical tasks.
- [View Phase 2 Report](docs/phase2_report.md)

## Repository Structure

```text
gem5_riscv_rt/
├── boards/               # Zephyr board definitions (DTS, Kconfig)
│   └── riscv/gem5_riscv32/
├── configs/              # gem5 configuration scripts (Python)
│   └── riscv_rt/         # Custom memory and system configs
├── docs/                 # Documentation and Reports
├── scripts/              # Automation scripts (Build, Run, Analyze)
├── src/                  # Source code (gem5, Zephyr submodules)
└── workloads/            # Real-time application source code
    └── automotive/
```

## Quick Start

### Prerequisites
- Linux (Ubuntu 22.04+ recommended)
- Python 3.10+
- Git, CMake, Ninja, DTC

### 1. Setup Environment
```bash
# Install dependencies
./scripts/install_dependencies.sh
./scripts/install_zephyr_deps.sh
./scripts/install_zephyr_sdk.sh
```

### 2. Build gem5
```bash
./scripts/build_gem5.sh
```

### 3. Build Workload
Build the mixed-criticality workload for the SRAM-based board:
```bash
./scripts/build_zephyr.sh gem5_riscv32 workloads/automotive/mixed_criticality
```

### 4. Run Simulation
Run a simulation using the SRAM boot mode and STT-MRAM main memory:
```bash
./scripts/run_sim.sh mixed_criticality src/zephyr/build/zephyr/zephyr.elf --boot-mode=sram --mem-tech=mram
```

### 5. View Results
Results (stats.txt, config.ini) are stored in `build/results/<experiment_name>`.
```bash
head build/results/mixed_criticality/zephyr/stats.txt
```

## License
This project is open-source. See individual submodules (gem5, Zephyr) for their respective licenses.
