# Implementation Plan: Phase 2 Memory Architecture Exploration

**Branch**: `002-memory-exploration` | **Date**: 2025-11-25 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/002-memory-exploration/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This phase implements advanced memory modeling (SRAM, NOR Flash, STT-MRAM) for the gem5 RISC-V simulation framework. It involves configuring the Ruby memory system for heterogeneous memory types, modifying the Zephyr board definition to support SRAM booting and mixed workloads, and extending the automation pipeline to support Design Space Exploration (DSE) of memory hierarchies.

## Technical Context

**Language/Version**: Python 3.10+ (gem5 scripts), C (Zephyr workloads), C++17 (gem5 source)
**Primary Dependencies**: gem5 v25.0, Zephyr SDK 0.16+
**Storage**: N/A (Simulation artifacts only)
**Testing**: gem5 simulation scripts, Zephyr QEMU emulation
**Target Platform**: Linux (Host), RISC-V 32-bit (Guest)
**Project Type**: Simulation Framework & Embedded Firmware
**Performance Goals**: Accurate latency modeling for SRAM/DRAM/NVM; Simulation speed > 100 KIPS
**Constraints**: 
- Must support gem5's Ruby memory system (or justify Classic fallback)
- Zephyr must boot from non-standard memory map (SRAM)
- STT-MRAM model must reflect asymmetric R/W latency

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Spec-Driven**: All requirements documented in spec before implementation begins
- [x] **Unambiguous**: Requirements use concrete numbers/conditions (no vague terms like "fast", "moderate")
- [x] **Testable**: Each requirement has defined verification method (test/measurement/simulation)
- [x] **Traceable**: Requirement IDs map to implementation files and test/simulation results
- [x] **Design First**: Correctness and reproducibility prioritized; optimization deferred to separate spec
- [x] **Atomic Commits**: Commit strategy defined (one logical change per commit)
- [x] **Source-Build Separation**: Build outputs confined to `build/` directory, source in `src/`
- [x] **Submodule Versions**: External dependencies (gem5, Zephyr, NVMain) pinned to specific versions
- [x] **Build Script Standards**: Dedicated build scripts log to files, errors to stdout
- [x] **Linux Text Standards**: LF line endings, files end with newline, UTF-8 encoding

## Project Structure

### Documentation (this feature)

```text
specs/002-memory-exploration/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output (Memory Map)
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (Config APIs)
└── tasks.md             # Phase 2 output
```

### Source Code (repository root)

```text
src/
├── gem5/                # Submodule
├── zephyr/              # Submodule
└── gem5_riscv_rt/       # (Conceptually, the repo root)

configs/
└── riscv_rt/
    ├── ruby/            # [NEW] Ruby configuration scripts
    └── memory.py        # [NEW] Memory hierarchy definitions

workloads/
└── automotive/
    └── mixed_criticality/ # [NEW] Mixed SRAM/DRAM workload

boards/
└── riscv/
    └── gem5_riscv32/
        ├── gem5_riscv32_sram.dts # [NEW] SRAM boot DTS
        └── Kconfig.defconfig     # Updated for SRAM support

scripts/
├── run_dse.sh           # [NEW] Design Space Exploration script
└── postprocess_dse.py   # [NEW] Extended metrics extractor
```

**Structure Decision**: Extending the existing repository structure. Adding `configs/riscv_rt/ruby` for advanced memory configs and `workloads/automotive/mixed_criticality` for new workloads.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| N/A | | |
