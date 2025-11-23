# gem5 RISC-V Full-System Simulation Architecture

## Overview

This project uses gem5 to perform full-system RISC-V 32-bit simulation for automotive real-time workload analysis and design-space exploration (DSE).

## System Components

```
┌─────────────────────────────────────────────────────────┐
│                    gem5 Simulator                        │
│  ┌────────────────────────────────────────────────────┐ │
│  │  RISC-V 32-bit In-Order CPU (500 MHz)             │ │
│  │  - RV32IMAC ISA                                    │ │
│  │  - MinorCPU (in-order pipeline)                    │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Memory Hierarchy                                  │ │
│  │  ├─ L1 I-Cache: 32 KB                             │ │
│  │  ├─ L1 D-Cache: 32 KB                             │ │
│  │  ├─ L2 Unified Cache: 256 KB                      │ │
│  │  └─ DRAM: 128 MB                                   │ │
│  └────────────────────────────────────────────────────┘ │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Peripherals                                       │ │
│  │  ├─ UART (serial console)                         │ │
│  │  └─ Timer                                          │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────────┐
│               Zephyr RTOS (RV32 target)                  │
│  ┌────────────────────────────────────────────────────┐ │
│  │  Automotive Workload                               │ │
│  │  - Periodic control loop (1ms period/deadline)     │ │
│  │  - Sensor simulation (ISR)                         │ │
│  │  - Control algorithm (PID/state machine)           │ │
│  │  - Timing measurements (k_cycle_get_32)            │ │
│  └────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────┘
```

## Baseline Configuration

### CPU
- **Architecture**: RISC-V 32-bit (RV32IMAC)
- **Implementation**: In-order (MinorCPU)
- **Frequency**: 500 MHz
- **Pipeline**: In-order execution, minimal speculation

### Cache Hierarchy
- **L1 Instruction Cache**: 32 KB
- **L1 Data Cache**: 32 KB
- **L2 Unified Cache**: 256 KB
- **Cache Line Size**: 64 bytes (typical)
- **Write Policy**: Write-back (configurable)

### Memory System
- **Main Memory**: 128 MB DRAM
- **Memory Technology**: SimpleDRAM (Phase 1), STT-MRAM (Phase 2)
- **Address Range**: 0x80000000 - 0x88000000

### Workload
- **RTOS**: Zephyr (RISC-V 32-bit target)
- **Task**: Periodic control loop
  - Period: 1 ms
  - Deadline: 1 ms
  - Priority: High
- **Timing**: Cycle-accurate measurement via Zephyr kernel APIs

## Repository Structure

```
gem5_riscv_rt/
├── src/                  # External source (submodules)
│   ├── gem5/            # gem5 simulator (submodule)
│   ├── zephyr/          # Zephyr RTOS (submodule/west install)
│   └── nvmain/          # (Phase 2) NVMain for STT-MRAM
├── configs/             # gem5 configuration scripts
│   └── riscv_rt/
│       ├── base_fs.py   # Baseline full-system config
│       └── params/      # Parameter definitions
├── workloads/           # Automotive workload code
│   ├── automotive/
│   │   └── control_loop/  # Periodic control task (Zephyr app)
│   └── bare_metal/      # Simple test programs
├── scripts/             # Build and automation scripts
│   ├── check_env.sh     # Environment validation
│   ├── build_gem5.sh    # gem5 build script
│   ├── build_zephyr.sh  # Zephyr build script
│   ├── run_sim.sh       # Simulation runner
│   └── postprocess_baseline.py  # Statistics parser
├── docs/                # Documentation
│   ├── ARCHITECTURE.md  # This file
│   ├── EXTERNALS.md     # External dependency documentation
│   ├── workloads/       # Workload specifications
│   └── results/         # Experiment results (CSV)
├── build/               # Build outputs (gitignored)
│   ├── gem5/
│   ├── zephyr/
│   └── results/
└── .specify/            # Specification framework
```

## Development Workflow

### Phase 1: Baseline Establishment
1. **M1**: Setup repository and toolchain
2. **M2**: Build gem5 and create baseline configuration
3. **M3**: Boot Zephyr RTOS on gem5
4. **M4**: Run automotive workload
5. **M5**: Automate metrics collection

### Phase 2+: Design Space Exploration
- STT-MRAM integration via NVMain
- TCM/TIM configuration analysis
- Cache/memory parameter sweeps
- Advanced workload scenarios

## Key Technologies

- **Simulator**: gem5 (RISC-V full-system)
- **RTOS**: Zephyr (RV32 target)
- **Toolchain**: RISC-V GNU toolchain (32-bit)
- **Build Tools**: Python 3.11+, SCons (gem5), west (Zephyr), cmake
- **Platform**: Ubuntu 24.04 LTS

## Metrics Collected

- **Performance**: Instructions Per Cycle (IPC), execution time
- **Cache**: Miss rates (L1-I, L1-D, L2), hit rates, average access latency
- **Memory**: Access latency (avg/max), bandwidth utilization
- **Real-Time**: Task response time, deadline miss rate, timing variability

## Out-of-Tree Builds

All builds execute in `build/` subdirectories:
- `build/gem5/` - gem5 binaries and build logs
- `build/zephyr/` - Zephyr application builds
- `build/results/<config>/<workload>/` - Simulation results

Source directories (`src/`, `configs/`, `workloads/`) remain read-only during builds.

## References

- gem5: https://www.gem5.org/
- Zephyr RTOS: https://www.zephyrproject.org/
- RISC-V ISA: https://riscv.org/
- NVMain: https://github.com/SEAL-UCSB/NVmain (Phase 2)
