# Implementation Plan: gem5 RISC-V Full-System Simulation Framework

**Branch**: `001-fullsystem-simulation` | **Date**: 2025-11-23 | **Spec**: [spec.md](file:///home/ubuntu/work/gem5/gem5_riscv_rt/specs/001-fullsystem-simulation/spec.md)  
**Input**: Feature specification from `/specs/001-fullsystem-simulation/spec.md`

## Summary

This plan implements Phase 1 of the gem5 RISC-V Full-System Simulation Framework, establishing a baseline simulation environment for automotive design-space exploration. The phase focuses on creating a working RISC-V 32-bit full-system simulation with Zephyr RTOS and automotive workload support, laying the foundation for future cache/memory parameter sweeps and STT-MRAM integration.

**Primary deliverables:**
1. Functional development environment (gem5, Zephyr, toolchains)
2. RISC-V 32-bit baseline configuration (500 MHz CPU, 32KB L1 caches, 256KB L2, 128MB DRAM)
3. Zephyr RTOS boot on gem5 full-system
4. Automotive periodic control loop workload (1ms period/deadline)
5. Automated experiment pipeline with metrics collection

## Technical Context

**Language/Version**: Python 3.11+ (gem5 configs/scripts), C (Zephyr/workloads), Shell (build scripts)  
**Primary Dependencies**: gem5 (RISC-V full-system), Zephyr RTOS, RISC-V GNU toolchain, west (Zephyr build tool)  
**Storage**: File-based (gem5 stats, Zephyr logs, experiment results in CSV/JSON)  
**Testing**: Manual verification (boot success, workload execution), smoke tests (build success), stat collection validation  
**Target Platform**: Ubuntu 24.04 LTS  
**Project Type**: Single embedded system project  
**Performance Goals**: 
- Zephyr boot within reasonable simulation time (minutes to hours)
- 1ms periodic task execution with deadline compliance
- Statistics collection overhead < 5% simulation slowdown  
**Constraints**: 
- Build time for all components < 2 hours (excluding gem5 build)
- Reproducible results (5% variance threshold)
- Out-of-tree builds only (no source tree pollution)  
**Scale/Scope**: 
- Single RISC-V core configuration
- 1-2 automotive workloads
- 3+ configuration variants for baseline comparison

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven**: All requirements documented in spec before implementation begins
- [x] **Unambiguous**: Requirements use concrete numbers/conditions (500 MHz, 32KB caches, 1ms period)
- [x] **Testable**: Each requirement has defined verification method (boot success, stat collection, workload execution)
- [x] **Traceable**: Requirement IDs (SYS-*, CPU-*, CACHE-*, etc.) map to implementation milestones
- [x] **Design First**: Phase 1 focuses on correctness (baseline working); optimization deferred to Phase 2
- [x] **Atomic Commits**: Each milestone produces atomic commits
- [x] **Source-Build Separation**: Build outputs confined to `build/` directory, source in `src/`
- [x] **Submodule Versions**: gem5, Zephyr versions will be pinned in M1-003
- [x] **Build Script Standards**: Dedicated build scripts (`build_gem5.sh`, `build_zephyr.sh`) with file logging
- [x] **Linux Text Standards**: All files use LF line endings, trailing newline, UTF-8 encoding

**Gate Result**: ✅ **PASSED** - All constitution requirements satisfied. Phase 1 scope is conservative, focused on baseline establishment.

## Project Structure

### Documentation (this feature)

```text
specs/001-fullsystem-simulation/
├── plan.md              # This file (/speckit.plan command output)
├── spec.md              # Feature specification
├── research.md          # Phase 0 output (to be created)
├── checklists/          
│   └── requirements.md  # Quality checklist
└── (Phase 1 outputs TBD: data-model.md, contracts/, quickstart.md)
```

### Source Code (repository root)

```text
gem5_riscv_rt/
├── src/                 # Source code (read-only during builds)
│   ├── gem5/           # gem5 submodule (tag/commit TBD in M1-003)
│   ├── zephyr/         # Zephyr RTOS submodule
│   └── nvmain/         # (Optional) NVMain for Phase 2
├── configs/            # gem5 configuration scripts
│   └── riscv_rt/       
│       ├── base_fs.py  # Baseline full-system config (M2-002)
│       └── params/     # Parameter definitions
├── workloads/          # Automotive workload definitions
│   └── automotive/
│       ├── control_loop/  # Periodic control task
│       └── microbench/    # CoreMark or similar
├── scripts/            # Build/run/analysis automation
│   ├── check_env.sh    # Environment validation (M1-002)
│   ├── build_gem5.sh   # gem5 build script (M2-001)
│   ├── build_zephyr.sh # Zephyr build script (M3-001)
│   ├── run_sim.sh      # Simulation runner  (M5-001)
│   └── postprocess_baseline.py  # Stats parser (M5-002)
├── docs/               # Documentation
│   ├── ARCHITECTURE.md # System overview (M1-001)
│   ├── EXTERNALS.md    # External dependency docs (M1-003)
│   ├── workloads/
│   │   └── automotive_baseline.md  # Workload spec (M4-001)
│   ├── results/        # Experiment results
│   │   └── baseline_summary.csv
│   └── phase1_report.md  # Phase 1 summary (M5-003)
├── build/              # All build outputs (gitignored)
│   ├── gem5/
│   │   ├── build/      # gem5 binaries
│   │   └── build.log   # Build log file
│   ├── zephyr/
│   │   └── build.log
│   └── results/
│       └── <config>/<workload>/  # Simulation results
└── .specify/           # Specification framework
```

**Structure Decision**: Using single project structure as this is an embedded system simulation project focused on gem5/Zephyr integration, not a web/mobile application.

## Phase 1: Baseline RISC-V Full-System Implementation

### Phase Scope

**Phase name**: Phase 1 – Baseline RISC-V Full-System Simulation  
**Timebox**: 2–4 weeks (priorities define order, not fixed dates)  

**Goals:**
1. Set up Ubuntu 24.04 development environment with gem5, Zephyr, RISC-V toolchain
2. Boot Zephyr RTOS on gem5 RISC-V 32-bit full-system (baseline config: 500 MHz, 32KB L1, 256KB L2, 128MB DRAM)
3. Execute at least one automotive periodic control loop workload (1ms period/deadline)
4. Create automated experiment pipeline for statistics collection (IPC, cache miss rates, memory latency, task timing)

**Out of Scope (Phase 2+):**
- STT-MRAM / NVMain detailed integration
- Static WCET analysis and safety-grade analysis
- Multi-core/lockstep configurations
- TCM/TIM detailed tuning
- Parameter sweep automation

### Milestones Overview

- **M1: Repository & Toolchain Skeleton Ready** (Priority: P0)
- **M2: gem5 RISC-V Full-System Baseline** (Priority: P0)
- **M3: Zephyr RTOS Boots on gem5 RISC-V** (Priority: P0)
- **M4: Automotive Workload Execution** (Priority: P1)
- **M5: Basic Experiment & Metrics Pipeline** (Priority: P1)

**Dependencies**: M1 → M2 → M3 → M4 → M5 (linear sequence for Phase 1)

---

### Milestone M1: Repository & Toolchain Skeleton Ready

**Goal**: Establish constitution-compliant directory structure and verify all required development tools are installed.

**Tasks:**

#### M1-001: Initialize Top-Level Directory Structure
- **Action**: Create `src/`, `configs/`, `workloads/`, `scripts/`, `docs/`, `build/` directories
- **Action**: Add `.gitignore` rules for `build/`, `*.log`, `*.pyc`, etc.
- **Action**: Create `docs/ARCHITECTURE.md` with system overview diagram and component descriptions
- **Verification**: 
  - `tree -L 2` shows expected directory structure
  - `docs/ARCHITECTURE.md` exists and contains baseline system diagram
- **Requirements**: REPO-001, BUILD-002

#### M1-002: Install and Verify Development Tools
- **Action**: Install on Ubuntu 24.04:
  - Python 3.11+, pip, cmake, ninja
  - RISC-V GNU toolchain (32-bit support)
  - git, git-lfs
  - Zephyr dependencies (west, dtc, etc.)
- **Action**: Create `scripts/check_env.sh` to verify:
  ```bash
  python3 --version >= 3.11
  riscv32-unknown-elf-gcc --version
  cmake --version >= 3.20
  west --version
  ```
- **Verification**: `scripts/check_env.sh` exits with code 0 and prints "✓ All tools OK"
- **Requirements**: BUILD-004

#### M1-003: Configure External Project Submodules
- **Action**: Add gem5 as submodule to `src/gem5/`:
  ```bash
  git submodule add https://github.com/gem5/gem5.git src/gem5
  cd src/gem5 && git checkout <specific-tag> # e.g., v23.1
  ```
- **Action**: Add Zephyr RTOS to `src/zephyr/` (document west workflow)
- **Action**: (Optional) Document NVMain setup for Phase 2
- **Action**: Create `docs/EXTERNALS.md` documenting:
  - Component name, origin URL, license, pinned version
  - Build dependencies and configuration notes
- **Verification**:
  - `git submodule status` shows pinned commits
  - `docs/EXTERNALS.md` lists all external components with licenses
- **Requirements**: REPO-002, REPO-003

**Milestone M1 DoD**:
- Directory structure matches constitution layout
- All dev tools installed and verified
- External dependencies documented and pinned

---

### Milestone M2: gem5 RISC-V Full-System Baseline

**Goal**: Build gem5 with RISC-V support and create a minimal full-system configuration that can simulate a simple program.

**Tasks:**

#### M2-001: Build gem5 for RISC-V Architecture
- **Action**: Create `scripts/build_gem5.sh`:
  ```bash
  #!/bin/bash
  cd src/gem5
  scons build/RISCV/gem5.opt -j$(nproc) 2>&1 | tee ../../build/gem5/build.log
  # Only print errors to stdout
  grep -i error ../../build/gem5/build.log || echo "✓ gem5 build successful"
  ```
- **Action**: Execute build script and verify binary creation
- **Verification**:
  - `build/gem5/build/RISCV/gem5.opt` exists
  - `./build/gem5/build/RISCV/gem5.opt --version` prints gem5 version
  - `build/gem5/build.log` contains full build output
- **Requirements**: BUILD-001, BUILD-003, Principle VI (Build Script Standards)

#### M2-002: Create Baseline Full-System Configuration
- **Action**: Create `configs/riscv_rt/base_fs.py` with:
  ```python
  # RISC-V 32-bit in-order CPU
  class BaseRISCV32System(System):
      cpu = RISCVO3CPU()  # Or MinorCPU for in-order
      cpu.clock = "500MHz"  # From clarification
      
      # Memory hierarchy
      cpu.icache = L1ICache(size="32kB")  # From clarification
      cpu.dcache = L1DCache(size="32kB")
      l2cache = L2Cache(size="256kB")     # From clarification
      
      # DRAM
      mem_ranges = [AddrRange("128MB")]   # From clarification
      mem_ctrl = SimpleMemory()
  ```
- **Action**: Add minimal device tree for serial console
- **Verification**:
  - Config script runs without syntax errors: `python3 configs/riscv_rt/base_fs.py --help`
  - Parameters match baseline from clarifications (500MHz, 32KB L1, 256KB L2, 128MB)
- **Requirements**: CPU-001, CPU-004, CACHE-001, MEM-001

#### M2-003: Validate Baseline with Bare-Metal Program
- **Action**: Create simple bare-metal "Hello RISC-V" program:
  ```c
  void _start() {
      volatile char *uart = (char *)0x10000000;
      char *msg = "Hello from RISC-V\n";
      while (*msg) *uart++ = *msg++;
      while(1);
  }
  ```
- **Action**: Compile and link for RISC-V 32-bit, load into gem5 memory
- **Action**: Run with `gem5.opt configs/riscv_rt/base_fs.py --kernel=<bare-metal-elf>`
- **Verification**:
  - gem5 simulation completes without crash
  - Serial output contains "Hello from RISC-V"
  - `m5out/stats.txt` file generated with basic CPU/cache statistics
- **Requirements**: SYS-001, SYS-007

**Milestone M2 DoD**:
- gem5 built successfully for RISC-V
- Baseline configuration matches specification values
- Simple program executes and produces stats

---

### Milestone M3: Zephyr RTOS Boots on gem5 RISC-V

**Goal**: Port/configure Zephyr RTOS to boot on gem5 RISC-V 32-bit full-system simulation.

**Tasks:**

#### M3-001: Set Up Zephyr Build Environment
- **Action**: Install Zephyr SDK and west tool
- **Action**: Create `scripts/build_zephyr.sh`:
  ```bash
  #!/bin/bash
  cd src/zephyr
  west build -b qemu_riscv32 samples/hello_world 2>&1 | tee ../../build/zephyr/build.log
  grep -i error ../../build/zephyr/build.log || echo "✓ Zephyr build successful"
  ```
- **Action**: Verify Zephyr builds for QEMU RISC-V32 target
- **Verification**:
  - `west build` completes successfully
  - QEMU can run hello_world sample and print "Hello World!"
  - `build/zephyr/build.log` contains full output
- **Requirements**: SW-001, BUILD-001, Principle VI

#### M3-002: Configure Zephyr for gem5 Target
- **Action**: Create custom Zephyr board definition or adapt existing RISC-V board:
  - Memory map matching gem5 baseline (0x80000000 start, 128MB size)
  - UART address matching gem5 device tree
  - Linker script for RISC-V 32-bit
- **Action**: Modify device tree and Kconfig for gem5 compatibility
- **Verification**:
  - Zephyr builds for gem5 target without errors
  - Generated ELF binary has correct load addresses
- **Requirements**: SW-001, CPU-001

#### M3-003: Boot Zephyr on gem5
- **Action**: Integrate Zephyr ELF with gem5 full-system config
- **Action**: Configure gem5 to load Zephyr kernel at correct address
- **Action**: Run simulation: `gem5.opt configs/riscv_rt/base_fs.py --kernel=zephyr.elf`
- **Verification**:
  - gem5 simulation starts without errors
  - Serial console shows "*** Booting Zephyr OS" banner
  - Zephyr shell prompt appears (if enabled) or hello_world message prints
  - gem5 stats include boot phase metrics
- **Requirements**: SYS-005, SC-002

**Milestone M3 DoD**:
- Zephyr builds for gem5 RISC-V target
- Zephyr boots successfully on gem5 full-system
- Boot log and statistics collected

---

### Milestone M4: Automotive Workload Execution

**Goal**: Implement and run an automotive periodic control loop on Zephyr/gem5 with real-time property measurement.

**Tasks:**

#### M4-001: Specify Automotive Workload Requirements
- **Action**: Create `docs/workloads/automotive_baseline.md` with:
  - Task structure: Periodic control task (1ms period/deadline from clarifications)
  - Background monitoring task (lower priority)
  - Simulated sensor ISR (interrupt every 1ms)
  - Pseudo-code for control algorithm (simple PID or state update)
- **Action**: Define timing measurement points (task start, end, ISR latency)
- **Verification**: Document reviewed and approved (or self-reviewed against SW-004)
- **Requirements**: SW-002, SW-004

#### M4-002: Implement Zephyr Automotive Application
- **Action**: Create Zephyr app in `workloads/automotive/control_loop/`:
  ```c
  void control_task(void) {
      while (1) {
          k_timer_status_sync(&control_timer);
          // Read sensor (simulated)
          // Compute control output (simple math)
          // Write actuator (simulated)
          log_timestamp("control_task_done");
      }
  }
  ```
- **Action**: Configure task priority and timing using Zephyr kernel APIs
- **Action**: Add timestamp logging using `k_cycle_get_32()` for timing measurement
- **Verification**:
  - App builds without errors
  - App runs on QEMU RISC-V32 and prints periodic task logs
  - Timestamps show ~1ms intervals (within Zephyr scheduling tolerance)
- **Requirements**: SW-002, SW-004, SW-005

#### M4-003: Execute Workload on gem5 and Collect Timing Data
- **Action**: Build automotive workload for gem5 target
- **Action**: Run simulation with extended duration (e.g., 1000 task iterations)
- **Action**: Extract timing data from Zephyr logs:
  - Task response time (start to completion)
  - Inter-arrival time distribution
  - Deadline miss count
- **Verification**:
  - Workload executes without crash for >= 1000 iterations
  - Log file contains timestamp arrays for analysis
  - Response times fall within deadline (1ms) for >= 95% of iterations
  - gem5 stats show workload-specific cache/memory behavior
- **Requirements**: SYS-006, SC-009, EXP-006

**Milestone M4 DoD**:
- Automotive workload spec documented
- Workload runs on gem5/Zephyr
- Timing characteristics measured and validated

---

### Milestone M5: Basic Experiment & Metrics Pipeline

**Goal**: Automate the simulation execution and statistics collection process for baseline configuration.

**Tasks:**

#### M5-001: Create Unified Simulation Runner Script
- **Action**: Create `scripts/run_sim.sh`:
  ```bash
  #!/bin/bash
  CONFIG=$1  # e.g., "baseline"
  WORKLOAD=$2  # e.g., "control_loop"
  
  OUTDIR=build/results/$CONFIG/$WORKLOAD
  mkdir -p $OUTDIR
  
  ./build/gem5/build/RISCV/gem5.opt \
    -d $OUTDIR \
    configs/riscv_rt/base_fs.py \
    --kernel=workloads/$WORKLOAD/zephyr.elf \
    2>&1 | tee $OUTDIR/sim.log
  
  echo "Results saved to $OUTDIR"
  ```
- **Action**: Add error handling and exit codes
- **Verification**:
  - `./scripts/run_sim.sh baseline control_loop` executes successfully
  - Results directory created at `build/results/baseline/control_loop/`
  - Contains: `stats.txt`, `config.ini`, `sim.log`, `terminal`
- **Requirements**: SYS-007, EXP-002, BUILD-001

#### M5-002: Implement Statistics Parser
- **Action**: Create `scripts/postprocess_baseline.py`:
  ```python
  import re
  
  def parse_gem5_stats(stats_file):
      stats = {}
      with open(stats_file) as f:
          stats['ipc'] = extract_stat(f, 'system.cpu.ipc')
          stats['l1i_miss_rate'] = extract_stat(f, 'system.cpu.icache.missRate')
          stats['l1d_miss_rate'] = extract_stat(f, 'system.cpu.dcache.missRate')
          stats['l2_miss_rate'] = extract_stat(f, 'system.l2cache.missRate')
          stats['mem_latency_avg'] = extract_stat(f, 'system.mem_ctrl.avgRdLatency')
      return stats
  
  def parse_zephyr_log(log_file):
      # Extract task timing data
      timestamps = extract_timestamps(log_file, 'control_task_done')
      response_times = compute_response_times(timestamps)
      return {
          'avg_response_time': mean(response_times),
          'max_response_time': max(response_times),
          'deadline_misses': count_misses(response_times, deadline=1000000)  # 1ms in cycles
      }
  ```
- **Action**: Output combined stats to CSV: `docs/results/baseline_summary.csv`
- **Verification**:
  - Script runs without errors on M5-001 output
  - CSV contains expected columns: IPC, L1I/L1D/L2 miss rates, memory latency, task timing
  - Values are reasonable (IPC > 0, miss rates 0-100%, latencies > 0)
- **Requirements**: EXP-003, EXP-004, SC-003, SC-010

#### M5-003: Generate Phase 1 Report
- **Action**: Create `docs/phase1_report.md` with:
  - Executive summary of Phase 1 achievements
  - System configuration table (CPU, cache, memory, workload)
  - Baseline performance metrics (table or chart)
  - Known limitations and Phase 2 preview (STT-MRAM, TCM, parameter sweeps)
  - Reproduction instructions (exact commands from clone to results)
- **Verification**:
  - Report exists and is complete
  - Another developer can follow instructions to reproduce results
- **Requirements**: SC-001, SC-004, SC-008

**Milestone M5 DoD**:
- Single command runs simulation and collects results
- Statistics automatically parsed to CSV
- Phase 1 report documents achievements

---

## Phase 1 Definition of Done

**Phase 1 is complete when all of the following are true:**

1. ✅ Repository cloned and submodules initialized: `git clone && git submodule update --init`
2. ✅ Environment check passes: `scripts/check_env.sh` → OK
3. ✅ gem5 builds successfully: `scripts/build_gem5.sh` → no errors, binary created
4. ✅ Zephyr builds successfully: `scripts/build_zephyr.sh` → ELF for gem5 target
5. ✅ Baseline simulation runs: `scripts/run_sim.sh baseline control_loop` → completes without crash
6. ✅ Zephyr boots on gem5 and automotive workload executes (>= 1000 iterations)
7. ✅ Results collected: `build/results/baseline/control_loop/` contains stats.txt, logs
8. ✅ Statistics parsed: `scripts/postprocess_baseline.py` → `docs/results/baseline_summary.csv`
9. ✅ Baseline metrics meet success criteria:
   - IPC, cache miss rates, memory latency recorded (SC-003)
   - Task deadlines met in >= 95% of iterations (SC-009)
   - Results reproducible within 5% variance (SC-007)
10. ✅ Phase 1 report complete: `docs/phase1_report.md` with reproduction instructions

**When all items above are checked, Phase 1 is DONE and Phase 2 can begin.**

## Phase 2+ Preview

Phase 2 will build on this baseline with:
- **STT-MRAM Integration**: NVMain setup, hybrid DRAM+STT-MRAM configurations (MEM-001)
- **TCM Configuration**: Code/data TCM implementation, variability analysis (TCM-001, TCM-002)
- **Parameter Sweeps**: Automated cache size/associativity/memory type sweeps (CACHE-003, EXP-001)
- **Advanced Workloads**: Additional automotive benchmarks, multi-task scenarios
- **Real-Time Analysis**: Deadline miss analysis, worst-case execution time characterization

Phase 1 establishes the foundation; Phase 2 explores the design space.

## Verification Plan

### Build Verification
- **Smoke Tests**: Each build script (`build_gem5.sh`, `build_zephyr.sh`) runs successfully
- **Command**: 
  ```bash
  ./scripts/build_gem5.sh && echo "gem5 OK"
  ./scripts/build_zephyr.sh && echo "Zephyr OK"
  ```
- **Expected**: Both print "OK", exit code 0, log files in `build/` contain no errors

### Functional Verification  
- **Zephyr Boot Test**: 
  - Command: `./scripts/run_sim.sh baseline hello_world`
  - Expected: gem5 terminal output contains "*** Booting Zephyr OS"
- **Automotive Workload Test**:
  - Command: `./scripts/run_sim.sh baseline control_loop`
  - Expected: Simulation completes, log shows >= 1000 task completions, deadline misses < 5%

### Metrics Verification
- **Statistics Validation**:
  - Command: `./scripts/postprocess_baseline.py build/results/baseline/control_loop/`
  - Expected: CSV generated with all required columns, values within expected ranges:
    - IPC: 0.1 - 2.0 (reasonable for in-order core)
    - L1 miss rate: 0.1% - 20% (workload dependent)
    - L2 miss rate: 0.01% - 5%
    - Avg memory latency: 50 - 500 cycles
    - Task response time: < 1ms (1,000,000 cycles @ 1GHz equivalent)

### Reproducibility Verification
- **Repeat Test**: Run same simulation twice
  - Command: 
    ```bash
    ./scripts/run_sim.sh baseline control_loop
    mv build/results/baseline/control_loop build/results/baseline/control_loop_run1
    ./scripts/run_sim.sh baseline control_loop
    mv build/results/baseline/control_loop build/results/baseline/control_loop_run2
    diff <(grep 'ipc' build/results/baseline/control_loop_run1/stats.txt) \
         <(grep 'ipc' build/results/baseline/control_loop_run2/stats.txt)
    ```
  - Expected: IPC values differ by < 5% (SC-007)

### Manual User Acceptance
- [ ] **User Review**: Baseline metrics (`docs/results/baseline_summary.csv`) reviewed and deemed reasonable for automotive workload
- [ ] **Phase 1 Report Approval**: `docs/phase1_report.md` provides sufficient detail for reproduction

**All verification steps above must pass before Phase 1 is considered complete.**
