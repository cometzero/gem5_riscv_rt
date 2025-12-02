# Tasks: Octa-Core AMP/SMP Cluster Configuration

## Phase 1: Setup
- [x] T001 Create `OctaHiFive` platform in `configs/riscv_rt/OctaHiFive.py`
- [x] T002 Create `fs_octa_hybrid.py` configuration script in `configs/riscv_rt/fs_octa_hybrid.py`
- [x] T003 Update `memory.py` to support shared MRAM/SRAM ranges in `configs/riscv_rt/memory.py`

## Phase 2: Foundational
- [x] T004 Update bootloader to support 8 cores (Park 5-7) in `src/bootloader/boot.S`
- [x] T005 Create Zephyr SMP overlay `gem5_smp.overlay` in `src/zephyr_apps/smp_hello/gem5_smp.overlay`
- [x] T006 Create Zephyr SMP application `smp_hello` in `src/zephyr_apps/smp_hello/src/main.c`

## Phase 3: User Story 1 (Hybrid Workload Execution)
- [x] T007 [US1] Build Zephyr AMP Kernels for Cores 0-3
- [x] T008 [US1] Build Zephyr SMP Kernel for Cluster 1 (Cores 4-7)
- [x] T009 [US1] Compile updated bootloader
- [x] T010 [US1] Run Octa-Core Simulation with `fs_octa_hybrid.py`
- [x] T011 [US1] Verify independent output from Cores 0-3
- [x] T012 [US1] Verify unified SMP output from Cluster 1 (UART4)

## Phase 4: User Story 2 (SMP Performance - Dining Philosophers)
- [ ] T013 [US2] Configure Zephyr Dining Philosophers Sample `smp_philosophers`
- [ ] T014 [US2] Run Simulation with Dining Philosophers workload
- [ ] T015 [US2] Analyze `m5out/stats.txt` and terminal output for deadlock-free execution

## Dependencies
- Phase 2 depends on Phase 1
- Phase 3 depends on Phase 2
- Phase 4 depends on Phase 3

## Implementation Strategy
- **MVP**: Get all 8 cores booting "Hello World" (Phase 3).
- **Refinement**: Run actual SMP Dining Philosophers workload (Phase 4).
