# Implementation Plan - Quad Core AMP Zephyr

**Feature**: Quad Core AMP Zephyr (`003-quad-core-amp`)
**Status**: Planning
**Spec**: [spec.md](spec.md)

## Goal Description

Implement a 4-core RISC-V Asymmetric Multi-Processing (AMP) simulation configuration in gem5. Each core will have dedicated 1MB SRAM and 2MB MRAM regions and run a separate Zephyr OS instance. The system will also provide 4 separate UARTs for independent console output.

## Technical Context

### Architecture
- **CPU**: 4x `TimingSimpleCPU` (RISC-V 32-bit)
- **Memory**:
  - 4x SRAM (1MB each)
  - 4x MRAM (2MB each, STT-MRAM model)
  - Boot ROM (Shared)
- **IO**:
  - 4x UART (HiFive compatible, mapped to distinct addresses)
- **Software**:
  - 4x Zephyr ELF binaries loaded via `Workload` object

### Dependencies
- Existing `configs/riscv_rt/memory.py` (STT-MRAM model)
- `src/dev/riscv/HiFive.py` (Platform definition to be extended/modified)

## Constitution Check

- [x] **Spec-Driven**: Feature is fully specified in `spec.md`.
- [x] **Unambiguous**: Memory map and UART config are explicitly defined.
- [x] **Design First**: `research.md` and `data-model.md` created before code.
- [x] **Atomic Commits**: Plan breaks down work into logical chunks.
- [x] **Source-Build Separation**: No build artifacts in source.

## Proposed Changes

### configs

#### [NEW] [fs_quad_amp.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/fs_quad_amp.py)
- New configuration script for the Quad Core AMP system.
- Instantiates 4 CPUs.
- Instantiates 4 memory pairs (SRAM/MRAM) using `memory.py` logic (refactored or called in loop).
- Configures `system.workload` to load 4 kernels.

#### [MODIFY] [memory.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/memory.py)
- Refactor `create_memory_system` to allow creating memory for a specific core (offset based) or make it more modular to support multiple instances.

#### [MODIFY] [base_fs.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/base_fs.py)
- (Optional) Might extract common setup logic if `fs_quad_amp.py` shares a lot.

### src/dev/riscv (Python)

#### [NEW] [QuadHiFive.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/QuadHiFive.py)
- Custom Platform class inheriting from `HiFive` (or similar) that defines 4 UARTs.
- *Note*: If we can't modify `src`, we will define this in `configs/riscv_rt/` as a local SimObject extension if possible, or just configure it in the script if the C++ object allows dynamic children.
- *Fallback*: If we cannot add children dynamically to C++ SimObjects from Python without rebuilding gem5, we might need to stick to 1 UART or modify the C++ source (which triggers a rebuild). **Assumption**: We can add extra UARTs in Python if they are just SimObjects attached to the bus.

## Verification Plan

### Automated Tests
- **Boot Test**:
  - Command: `./build/RISCV/gem5.opt configs/riscv_rt/fs_quad_amp.py --kernels tests/hello.elf,tests/hello.elf,tests/hello.elf,tests/hello.elf`
  - Verification: Check `m5out/system.pc.com_{1..4}.device` for "Hello World".

### Manual Verification
- Inspect `m5out/config.ini` to verify:
  - 4 CPUs created.
  - Memory ranges match the spec (0x30000000, 0x40000000, etc.).
  - 4 UARTs instantiated.
