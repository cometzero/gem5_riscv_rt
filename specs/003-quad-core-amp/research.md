# Research: Quad Core AMP Zephyr

**Feature**: Quad Core AMP Zephyr (`003-quad-core-amp`)
**Status**: Complete
**Date**: 2025-11-28

## Technical Context

The goal is to simulate a 4-core RISC-V AMP system where each core runs a separate Zephyr OS instance.
Key constraints:
- 4x RISC-V 32-bit cores
- Per-core memory: 1MB SRAM, 2MB MRAM
- Custom Memory Map: MRAM Base 0x30000000, SRAM Base 0x40000000
- 4 Separate UARTs
- Separate Zephyr binaries for each core

## Decisions & Rationale

### 1. Multi-Core Instantiation
**Decision**: Use a loop to instantiate 4 `TimingSimpleCPU` objects and assign them to `system.cpu`.
**Rationale**: Standard gem5 practice for multi-core. `TimingSimpleCPU` is robust for functional verification.
**Alternatives**: `MinorCPU` (more detailed, slower), `O3CPU` (too complex for this phase).

### 2. Memory Map & Controllers
**Decision**: Instantiate separate `SimpleMemory` (SRAM) and `MemCtrl` (MRAM) objects for each core, mapped to the specified non-overlapping ranges.
- Core 0: SRAM 0x40000000, MRAM 0x30000000
- Core 1: SRAM 0x40100000, MRAM 0x30200000
- ... and so on.
**Rationale**: Explicit mapping ensures isolation required for AMP.
**Alternatives**: Shared memory controller with partitioning (less realistic for "dedicated" memory requirement).

### 3. Boot Loading (Workload)
**Decision**: Use `RiscvBareMetal` workload. Assign a list of binaries if supported, or use a custom loader script/object if `RiscvBareMetal` only supports one.
*Correction*: `RiscvBareMetal` typically takes a single `bootloader` argument. For 4 cores, we might need to use `Workload` object per core if supported, or more likely, we will use the `workload` parameter on the `System` object which might expect a single kernel.
*Refined Decision*: We will attempt to assign a list of kernels to `system.workload` if the object supports it, or we might need to modify the bootloader (OpenSBI) to load separate payloads. However, the spec clarification accepted "Option A: Use gem5 Workload object to load 4 separate ELF binaries".
*Implementation Detail*: We will check if `system.workload` can accept a list or if we need to set `cpu[i].workload`.
**Rationale**: Spec requirement FR-006.

### 4. UART Configuration
**Decision**: The `HiFive` platform object in gem5 has a single UART. We need to extend or modify the platform configuration to add 3 more UART devices at different MMIO addresses.
**Rationale**: Spec requirement FR-007.
**Implementation**: We will likely need to define a custom Platform class inheriting from `HiFive` or `Platform` that adds `uart1`, `uart2`, `uart3`.

## Unknowns & Risks

- **Risk**: `RiscvBareMetal` might not support multiple binaries out of the box.
- **Mitigation**: If it fails, we will fallback to a single "multiboot" blob or investigate `Process` based assignment (though this is full system).
- **Risk**: Adding UARTs to `HiFive` might require modifying the C++ SimObject if the python class doesn't expose a list.
- **Mitigation**: Check `src/dev/riscv/HiFive.py` (if available) or `src/dev/riscv/HiFive.hh`. Since we can't see `src`, we will try to add them in Python and see if the SimObject builder accepts it.

## Verification Strategy

- **Boot Test**: Run simulation and grep for "Booting Zephyr" 4 times.
- **Memory Test**: Inspect memory map in `m5out/config.ini`.
