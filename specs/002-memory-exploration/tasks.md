# Tasks: Phase 2 Memory Architecture Exploration

**Feature**: Phase 2 Memory Architecture Exploration
**Branch**: `002-memory-exploration`
**Spec**: [spec.md](spec.md)

## Phase 1: Setup

- [ ] T001 Create Phase 2 directory structure in `configs/riscv_rt/ruby` and `workloads/automotive/mixed_criticality`
- [ ] T002 Rebuild gem5 with Ruby `MI_example` protocol support using `scripts/build_gem5.sh`

## Phase 2: Foundational (Memory System)

- [ ] T003 Create `configs/riscv_rt/memory.py` defining the physical memory map (SRAM, Flash, DRAM) for Classic Memory
- [ ] T004 Create `configs/riscv_rt/ruby/system.py` to configure Ruby `MI_example` with heterogeneous memory ranges
- [ ] T005 Create `boards/riscv/gem5_riscv32/gem5_riscv32_sram.dts` defining the SRAM-based memory map for Zephyr
- [ ] T006 Update `boards/riscv/gem5_riscv32/Kconfig.defconfig` to support the new SRAM board variant

## Phase 3: User Story 1 - SRAM Boot (SRAM2, FLASH2)

- [x] T007: Implement Flash (ROM) model at `0x20000000` in `configs/riscv_rt/memory.py` <!-- id: 7 -->
- [x] T008: Implement SRAM model at `0x80000000` in `configs/riscv_rt/memory.py` <!-- id: 8 -->
- [x] T009: Update `configs/riscv_rt/base_fs.py` to support `--boot-mode=sram` and map the kernel accordingly <!-- id: 9 -->
- [x] T010 [US1] Verify SRAM boot functionality using Classic Memory with a simple Zephyr Hello World
- [x] T011 [US1] Verify SRAM boot functionality using Ruby Memory with a simple Zephyr Hello World

## Phase 4: User Story 2 - Mixed Workloads (MIX)

- [ ] T012 [US2] Create `workloads/automotive/mixed_criticality/src/main.c` with critical and non-critical tasks
- [ ] T013 [US2] Define linker section macros for `.sram_text` and `.sram_data` in the workload source
- [ ] T014 [US2] Create `workloads/automotive/mixed_criticality/prj.conf` enabling required Zephyr features
- [ ] T015 [US2] Update Zephyr linker script (or use CMake) to map `.sram_text` to the SRAM region
- [ ] T016 [US2] Verify mixed workload execution: Critical task runs in SRAM, background in DRAM

## Phase 5: User Story 3 - STT-MRAM (STTM)

- [ ] T017 [US3] Implement `NVMInterface` configuration in `configs/riscv_rt/memory.py` for STT-MRAM
- [ ] T018 [US3] Implement Ruby `MemoryControl` parameters for STT-MRAM in `configs/riscv_rt/ruby/system.py`
- [ ] T019 [US3] Add `--mem-type` CLI argument to `configs/riscv_rt/base_fs.py` to switch between DRAM and MRAM
- [ ] T020 [US3] Verify STT-MRAM latency characteristics (Asymmetric R/W) in simulation stats

## Phase 6: Experiment & Polish (EXP2)

- [ ] T021 Create `scripts/run_dse.sh` to automate execution of CFG-A, CFG-B, and CFG-C configurations
- [ ] T022 Create `scripts/postprocess_dse.py` to extract memory-specific metrics (SRAM hits, MRAM latency)
- [ ] T023 Execute full DSE suite and generate Phase 2 Report in `docs/phase2_report.md`

## Dependencies

1. **Setup** (T001-T002) must complete first.
2. **Foundational** (T003-T006) blocks all User Stories.
3. **US1** (SRAM Boot) is required for **US2** (Mixed Workloads).
4. **US3** (STT-MRAM) is independent of US1/US2 but shares the memory config structure.
5. **EXP2** requires all User Stories to be complete.

## Implementation Strategy

1. **MVP**: Get SRAM boot working in Classic Memory first (T003, T005, T007-T010). This validates the Zephyr map.
2. **Ruby Integration**: Enable Ruby support (T002, T004, T011). This is the "Advanced" requirement.
3. **Workload**: Implement the mixed workload (T012-T016) to leverage the SRAM.
4. **NVM**: Add STT-MRAM support (T017-T020) as a drop-in replacement for DRAM.
5. **DSE**: Run the experiments.
