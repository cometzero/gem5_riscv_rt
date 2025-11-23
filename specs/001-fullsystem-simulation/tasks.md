---
description: "Task list for gem5 RISC-V Full-System Simulation Framework - Phase 1"
---

# Tasks: gem5 RISC-V Full-System Simulation Framework

**Input**: Design documents from `/specs/001-fullsystem-simulation/`  
**Prerequisites**: plan.md (Phase 1 implementation plan), spec.md (feature specification with milestones)

**Tests**: Tests are NOT included in Phase 1. Phase 1 focuses on establishing a working baseline. Testing will be manual verification at each milestone.

**Organization**: Tasks are grouped by milestone (M1-M5) following Phase 1 implementation plan. Each milestone is independently verifiable.

## Format: `[ID] [P?] [Milestone] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Milestone]**: Which milestone this task belongs to (M1, M2, M3, M4, M5)
- Include exact file paths in descriptions

## Path Conventions

This is a single embedded system project with structure:
- `src/` - External dependencies (gem5, Zephyr submodules)
- `configs/` - gem5 configuration scripts
- `workloads/` - Automotive workload code
- `scripts/` - Build and automation scripts
- `docs/` - Documentation
- `build/` - All build outputs (gitignored)

---

## Phase 1: Setup (Repository & Toolchain)

**Purpose**: Establish constitution-compliant directory structure and verify development tools

**Milestone**: M1 - Repository & Toolchain Skeleton Ready

- [x] T001 Create top-level directories: src/, configs/, workloads/, scripts/, docs/, build/
- [x] T002 Create .gitignore with build/, *.log, *.pyc, __pycache__, .vscode/, *.swp entries
- [x] T003 Create docs/ARCHITECTURE.md with system overview and baseline configuration diagram
- [x] T004 [P] Create scripts/check_env.sh to verify Python 3.11+, riscv32-unknown-elf-gcc, cmake, west
- [x] T005 [P] Document Ubuntu 24.04 package requirements in docs/ARCHITECTURE.md
- [x] T006 Add gem5 submodule: git submodule add https://github.com/gem5/gem5.git src/gem5
- [x] T007 Pin gem5 to stable tag: cd src/gem5 && git checkout <tag>
- [x] T008 Add Zephyr setup instructions to docs/EXTERNALS.md (west init, etc.)
- [x] T009 [P] Create docs/EXTERNALS.md documenting gem5, Zephyr, licenses, pinned versions
- [x] T010 Verify M1 completion: tree -L 2, scripts/check_env.sh passes, git submodule status

**Checkpoint**: Repository structure ready, tools verified, submodules pinned

---

## Phase 2: Foundational (gem5 Baseline Build)

**Purpose**: Build gem5 with RISC-V support - BLOCKS all subsequent milestones

**Milestone**: M2 - gem5 RISC-V Full-System Baseline

**⚠️ CRITICAL**: No other milestones can proceed until gem5 is built

- [ ] T011 Create scripts/build_gem5.sh with build command: scons build/RISCV/gem5.opt -j$(nproc)
- [ ] T012 Add logging to build_gem5.sh: 2>&1 | tee ../../build/gem5/build.log
- [ ] T013 Add error handling to build_gem5.sh: grep -i error on log, exit codes
- [ ] T014 Execute build_gem5.sh and verify build/gem5/build/RISCV/gem5.opt exists
- [ ] T015 Create configs/riscv_rt/ directory for configuration scripts
- [ ] T016 Create configs/riscv_rt/base_fs.py with MinorCPU, 500MHz, RV32IMAC
- [ ] T017 Add L1 caches to base_fs.py: L1ICache(32kB), L1DCache(32kB)
- [ ] T018 Add L2 cache to base_fs.py: L2Cache(256kB unified)
- [ ] T019 Add DRAM to base_fs.py: SimpleMemory(), AddrRange(128MB)
- [ ] T020 [P] Add serial console device tree to base_fs.py
- [ ] T021 Create workloads/bare_metal/ directory for test programs
- [ ] T022 Write workloads/bare_metal/hello.c with UART "Hello from RISC-V" output
- [ ] T023 Create workloads/bare_metal/Makefile for riscv32-unknown-elf-gcc compilation
- [ ] T024 Compile bare-metal hello.c to ELF binary
- [ ] T025 Create scripts/run_bare_metal.sh to run gem5 with hello.elf
- [ ] T026 Execute run_bare_metal.sh and verify "Hello from RISC-V" in terminal output
- [ ] T027 Verify m5out/stats.txt contains system.cpu.ipc, icache.missRate, dcache.missRate
- [ ] T028 Verify M2 completion: gem5 built, config matches baseline (500MHz, 32KB L1, 256KB L2), stats generated

**Checkpoint**: gem5 builds successfully, baseline configuration validated, simple program executes

---

## Phase 3: Milestone M3 - Zephyr RTOS Boot

**Purpose**: Port/configure Zephyr RTOS to boot on gem5 RISC-V full-system

**Independent Test**: Zephyr boots and prints "*** Booting Zephyr OS" banner in gem5 simulation

- [ ] T029 Install Zephyr SDK: download and extract to ~/zephyr-sdk
- [ ] T030 Install west tool: pip3 install west
- [ ] T031 Initialize Zephyr workspace: west init src/zephyr
- [ ] T032 Update Zephyr modules: cd src/zephyr && west update
- [ ] T033 Create scripts/build_zephyr.sh for west build command
- [ ] T034 Add logging to build_zephyr.sh: 2>&1 | tee ../../build/zephyr/build.log
- [ ] T035 Test Zephyr build for QEMU: west build -b qemu_riscv32 samples/hello_world
- [ ] T036 Verify QEMU run succeeds: west build -t run (in terminal, not gem5 yet)
- [ ] T037 Create custom board definition src/zephyr/boards/riscv/gem5_riscv32/ (or adapt existing)
- [ ] T038 Configure gem5_riscv32 memory map: start=0x80000000, size=128MB in DTS
- [ ] T039 Configure gem5_riscv32 UART address to match gem5 device tree
- [ ] T040 Create gem5_riscv32.dts device tree file with CPU, memory, UART nodes
- [ ] T041 Create gem5_riscv32_defconfig Kconfig file for board
- [ ] T042 Build Zephyr for gem5 target: west build -b gem5_riscv32 samples/hello_world
- [ ] T043 Verify Zephyr ELF has correct load addresses: readelf -l build/zephyr/zephyr.elf
- [ ] T044 Update configs/riscv_rt/base_fs.py to load Zephyr kernel at correct address
- [ ] T045 Create scripts/run_zephyr.sh to run gem5 with --kernel=zephyr.elf
- [ ] T046 Execute run_zephyr.sh and capture serial console output
- [ ] T047 Verify "*** Booting Zephyr OS" appears in terminal output
- [ ] T048 Verify Zephyr shell prompt (if enabled) or hello_world message appears
- [ ] T049 Verify gem5 stats include boot phase metrics (IPC, cache activity)
- [ ] T050 Verify M3 completion: Zephyr boots on gem5, boot log saved, stats collected

**Checkpoint**: Zephyr builds for gem5 target, boots successfully, verified via serial output

---

## Phase 4: Milestone M4 - Automotive Workload Execution

**Purpose**: Implement and run automotive periodic control loop on Zephyr/gem5

**Independent Test**: Control loop executes >= 1000 iterations with PER

IOD=1ms, >= 95% deadline compliance

- [ ] T051 Create docs/workloads/automotive_baseline.md documenting workload structure
- [ ] T052 Define periodic control task: period=1ms, deadline=1ms, priority=high
- [ ] T053 Define background monitoring task: lower priority, non-real-time
- [ ] T054 Define simulated sensor ISR: interrupt every 1ms
- [ ] T055 Add pseudo-code for PID controller or simple state update algorithm
- [ ] T056 Document timing measurement points: task start, task end, ISR latency
- [ ] T057 Create workloads/automotive/control_loop/ directory for Zephyr app
- [ ] T058 Create control_loop/src/main.c with Zephyr kernel API includes
- [ ] T059 [P] Create control_loop/CMakeLists.txt for Zephyr build system
- [ ] T060 Implement k_timer_define for 1ms periodic timer in main.c
- [ ] T061 Implement control_task() with k_timer_status_sync() for period enforcement
- [ ] T062 Add simulated sensor read (random number or counter) to control_task
- [ ] T063 Add simple control algorithm (PID or state machine) to control_task
- [ ] T064 Add simulated actuator write (printk or variable update) to control_task
- [ ] T065 Add timestamp logging using k_cycle_get_32() at task start and end
- [ ] T066 Implement sensor ISR with k_isr_direct() for interrupt handling
- [ ] T067 [P] Create control_loop/prj.conf with CONFIG_PRINTK, CONFIG_TIMERS enabled
- [ ] T068 Build control_loop for QEMU: west build -b qemu_riscv32 workloads/automotive/control_loop
- [ ] T069 Test on QEMU and verify periodic task logs at ~1ms intervals
- [ ] T070 Build control_loop for gem5: west build -b gem5_riscv32 workloads/automotive/control_loop
- [ ] T071 Create scripts/run_automotive.sh to run gem5 with control_loop workload
- [ ] T072 Configure simulation duration for >= 1000 task iterations (1 second simulated time)
- [ ] T073 Execute run_automotive.sh and let simulation run to completion
- [ ] T074 Extract timestamp data from terminal output or log file
- [ ] T075 Calculate task response times: end_timestamp - start_timestamp
- [ ] T076 Calculate inter-arrival times: start_timestamp[i+1] - start_timestamp[i]
- [ ] T077 Count deadline misses: response_time > 1ms in cycles (500k cycles @ 500MHz)
- [ ] T078 Verify >= 1000 task completions in log
- [ ] T079 Verify deadline miss rate < 5% (< 50 misses out of 1000)
- [ ] T080 Verify gem5 stats show workload cache/memory behavior
- [ ] T081 Verify M4 completion: workload runs >= 1000 iterations, timing measured, deadline compliance verified

**Checkpoint**: Automotive workload executes successfully, timing characteristics measured

---

## Phase 5: Milestone M5 - Experiment & Metrics Pipeline

**Purpose**: Automate simulation execution and statistics collection

**Independent Test**: Single command runs simulation and generates CSV with IPC, miss rates, latency, task timing

- [ ] T082 Create scripts/run_sim.sh with arguments: CONFIG=$1, WORKLOAD=$2
- [ ] T083 Add output directory creation: mkdir -p build/results/$CONFIG/$WORKLOAD
- [ ] T084 Add gem5 execution command: gem5.opt -d $OUTDIR configs/riscv_rt/base_fs.py --kernel=$WORKLOAD
- [ ] T085 Add simulation logging: 2>&1 | tee $OUTDIR/sim.log
- [ ] T086 Add error handling and exit codes to run_sim.sh
- [ ] T087 Add result path printing: echo "Results saved to $OUTDIR"
- [ ] T088 Test run_sim.sh: ./scripts/run_sim.sh baseline control_loop
- [ ] T089 Verify results directory created: build/results/baseline/control_loop/
- [ ] T090 Verify output files exist: stats.txt, config.ini, sim.log, terminal
- [ ] T091 Create scripts/postprocess_baseline.py with argparse for input directory
- [ ] T092 [P] Create docs/results/ directory for output CSVs
- [ ] T093 Implement parse_gem5_stats() function to extract IPC from stats.txt
- [ ] T094 Add L1 I-cache miss rate extraction to parse_gem5_stats()
- [ ] T095 Add L1 D-cache miss rate extraction to parse_gem5_stats()
- [ ] T096 Add L2 cache miss rate extraction to parse_gem5_stats()
- [ ] T097 Add average memory latency extraction to parse_gem5_stats()
- [ ] T098 Implement parse_zephyr_log() to extract timestamps from terminal/sim.log
- [ ] T099 Implement compute_response_times() to calculate task timing from timestamps
- [ ] T100 Add average response time calculation to parse_zephyr_log()
- [ ] T101 Add maximum response time calculation to parse_zephyr_log()
- [ ] T102 Add deadline miss count to parse_zephyr_log() (>1ms in cycles)
- [ ] T103 Implement CSV output: write combined stats to docs/results/baseline_summary.csv
- [ ] T104 Add CSV headers: Config,Workload,IPC,L1I_Miss,L1D_Miss,L2_Miss,Mem_Latency,Avg_Response,Max_Response,Deadline_Misses
- [ ] T105 Test postprocess_baseline.py on M5-001 simulation output
- [ ] T106 Verify CSV contains all expected columns with reasonable values
- [ ] T107 Verify IPC > 0, miss rates 0-100%, latencies > 0
- [ ] T108 Create docs/phase1_report.md with Phase 1 executive summary
- [ ] T109 Add system configuration table to phase1_report.md (CPU, cache, memory, workload params)
- [ ] T110 Add baseline performance metrics table/chart to phase1_report.md
- [ ] T111 Add known limitations section: STT-MRAM not integrated, TCM not configured, no sweeps
- [ ] T112 Add Phase 2 preview: STT-MRAM, TCM, parameter sweeps, advanced workloads
- [ ] T113 Add reproduction instructions to phase1_report.md: exact command sequence from clone to results
- [ ] T114 Test reproduction instructions: follow commands in clean environment (or document for manual verification)
- [ ] T115 Verify M5 completion: run_sim.sh works, postprocess generates CSV, phase1_report.md complete

**Checkpoint**: Automated pipeline runs simulation and collects all required metrics

---

## Phase 6: Polish & Validation

**Purpose**: Final checks and Phase 1 completion verification

- [ ] T116 [P] Run constitution compliance check: verify LF line endings in all text files
- [ ] T117 [P] Verify all files end with newline: find . -name "*.py" -o -name "*.sh" | xargs -I {} sh -c 'tail -c1 {} | od -An -tx1 | grep -q "0a" || echo "{} missing newline"'
- [ ] T118 [P] Verify build logs exist: ls build/gem5/build.log build/zephyr/build.log
- [ ] T119 [P] Verify all scripts have execute permissions: chmod +x scripts/*.sh
- [ ] T120 Run full Phase 1 pipeline test: clone, check-env, build-gem5, build-zephyr, run-sim, postprocess
- [ ] T121 Verify Phase 1 Definition of Done criterion 1: git clone + submodule update works
- [ ] T122 Verify Phase 1 DoD criterion 2: scripts/check_env.sh → OK
- [ ] T123 Verify Phase 1 DoD criterion 3: gem5 builds successfully
- [ ] T124 Verify Phase 1 DoD criterion 4: Zephyr builds for gem5 target
- [ ] T125 Verify Phase 1 DoD criterion 5: baseline simulation runs to completion
- [ ] T126 Verify Phase 1 DoD criterion 6: Zephyr boots, workload runs >= 1000 iterations
- [ ] T127 Verify Phase 1 DoD criterion 7: results in build/results/baseline/control_loop/
- [ ] T128 Verify Phase 1 DoD criterion 8: docs/results/baseline_summary.csv generated
- [ ] T129 Verify Phase 1 DoD criterion 9: metrics meet success criteria (IPC recorded, deadline compliance >= 95%)
- [ ] T130 Verify Phase 1 DoD criterion 10: docs/phase1_report.md complete with reproduction instructions
- [ ] T131 Run reproducibility test: execute simulation twice, compare IPC variance < 5%
- [ ] T132 Create Phase 1 completion summary: list all milestones achieved, metrics collected, DoD criteria met

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - start immediately ✅
- **Foundational (Phase 2)**: Depends on Setup (M1) completion - BLOCKS all milestones ⚠️
- **M3 (Zephyr Boot)**: Depends on Foundational (M2) - gem5 must be built
- **M4 (Automotive Workload)**: Depends on M3 - Zephyr must boot successfully
- **M5 (Metrics Pipeline)**: Depends on M4 - workload must execute to collect metrics
- **Polish (Phase 6)**: Depends on M5 completion

### Milestone Dependencies

- **M1 (Setup)**: No dependencies - can start immediately
- **M2 (gem5 Baseline)**: Depends on M1 (T001-T010 complete)
- **M3 (Zephyr Boot)**: Depends on M2 (T011-T028 complete)
- **M4 (Automotive Workload)**: Depends on M3 (T029-T050 complete)
- **M5 (Metrics Pipeline)**: Depends on M4 (T051-T081 complete)

### Task Dependencies Within Milestones

**M1 (Setup)**:
- T001-T005: Can run in parallel (different files)
- T006: Must complete before T007 (submodule must exist before pinning)
- T008-T009: Can run in parallel with T006-T007
- T010: Must be last (verification task)

**M2 (gem5 Baseline)**:
- T011-T014: Sequential (build script → execute → verify)
- T015-T020: Can run in parallel after T014 (config development)
- T021-T024: Sequential (create dir → write code → makefile → compile)
- T025-T028: Sequential (run script → execute → verify stats → verify M2)

**M3 (Zephyr Boot)**:
- T029-T032: Sequential (SDK → west → init → update)
- T033-T036: Sequential (build script → test QEMU)
- T037-T042: Sequential (board definition → build for gem5)
- T043-T050: Sequential (verify ELF → run on gem5 → verify boot)

**M4 (Automotive Workload)**:
- T051-T056: Can run in parallel (documentation tasks)
- T057-T059: Parallel (directory + files)
- T060-T067: Sequential (code development)
- T068-T069: Sequential (QEMU test)
- T070-T081: Sequential (gem5 build → run → analyze → verify)

**M5 (Metrics Pipeline)**:
- T082-T090: Sequential (script development → test → verify)
- T091-T092: Parallel (python script + results dir)
- T093-T107: Sequential (parser development → test → verify)
- T108-T115: Sequential (report writing → verify)

### Parallel Opportunities

- **M1**: T004, T005, T008, T009 can run in parallel
- **M2**: T015-T020 can run in parallel after gem5 is built
- **M3**: Limited parallelization (mostly sequential build/test cycle)
- **M4**: T057-T059, T067 can run in parallel
- **M5**: T091-T092 can run in parallel
- **Polish**: T116-T119 can run in parallel

---

## Implementation Strategy

### MVP First (Milestone M1-M3 Only)

For fastest path to a working simulation:

1. Complete Phase 1: Setup (T001-T010) → Repository ready
2. Complete Phase 2: gem5 Baseline (T011-T028) → gem5 works
3. Complete Phase 3: Zephyr Boot (T029-T050) → Zephyr boots
4. **STOP and VALIDATE**: Minimal working system achieved
5. Can demo: gem5 running Zephyr RTOS on RISC-V 32-bit

### Incremental Delivery (Full Phase 1)

For complete Phase 1 deliverables:

1. Setup + gem5 Baseline → Can run bare-metal programs
2. Add Zephyr Boot → Can run RTOS
3. Add Automotive Workload → Can run realistic workloads  
4. Add Metrics Pipeline → Can collect performance data
5. Polish → Phase 1 complete, ready for Phase 2

### Recommended Approach

- **Week 1**: M1 + M2 (Setup + gem5 baseline)
- **Week 2**: M3 (Zephyr boot validation)
- **Week 3**: M4 (Automotive workload development and testing)
- **Week 4**: M5 + Polish (Metrics pipeline and final validation)

---

## Notes

- All tasks include exact file paths for implementation clarity
- No test tasks included (manual verification at each milestone)
- Each milestone has independent verification criteria
- Milestone M2 blocks all subsequent work (must complete gem5 build first)
- Constitution compliance checks in final polish phase
- Reproducibility verification in final phase (5% variance threshold)
- Phase 1 DoD has 10 explicit criteria - all must pass

**Total Tasks**: 132 tasks across 6 phases (5 milestones + polish)

**Parallel Tasks**: ~15 tasks marked [P] can run concurrently with others

**Critical Path**: M1 → M2 → M3 → M4 → M5 → Polish (linear for Phase 1)
