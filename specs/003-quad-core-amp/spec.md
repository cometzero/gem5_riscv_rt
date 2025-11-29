# Feature Specification: Quad Core AMP Zephyr

**Feature Branch**: `003-quad-core-amp`
**Created**: 2025-11-27
**Status**: Draft
**Input**: User description: "이번에는 앞에서 만든 risc-v 32bit core를 4개로 구성하고자 합니다. SRAM과 MRAM으로만 구성되며 각 Core당 SRAM 1MB, MRAM은 2MB입니다. 각 Core에는 Zephyr OS를 AMP로 각각 구동합니다."

## Clarifications

### Session 2025-11-27

- Q: Memory Map Layout? → A: Custom (MRAM: 0x30000000, SRAM: 0x40000000)
- Q: Boot Loading Mechanism? → A: Option A (Use gem5 `Workload` object to load 4 separate ELF binaries)
- Q: UART Configuration? → A: Option B (4 Separate UARTs, one per core)

## User Scenarios & Testing

### User Story 1 - Simulate 4-Core AMP System (Priority: P1)

As an embedded developer, I want to configure and run a 4-core RISC-V simulation where each core has dedicated SRAM and MRAM and runs its own Zephyr OS instance, so that I can develop and test Asymmetric Multi-Processing (AMP) applications.

**Why this priority**: This is the core functionality requested. Without the multi-core configuration and memory setup, the feature cannot be used.

**Independent Test**: Can be fully tested by running the gem5 simulation with the new configuration and observing 4 distinct Zephyr boot sequences.

**Acceptance Scenarios**:

1. **Given** a compiled Zephyr image for the target platform, **When** I run the gem5 simulation with the 4-core configuration, **Then** the simulation should initialize 4 RISC-V cores.
2. **Given** the simulation is running, **When** the cores boot, **Then** each core should access its designated 1MB SRAM and 2MB MRAM regions without error.
3. **Given** the simulation is running, **When** the OS boots, **Then** I should see boot messages from Zephyr OS on all 4 cores (e.g., via multiplexed UART or separate terminals).

---

### Edge Cases

- What happens when a core attempts to access memory assigned to another core? (Assuming flat address space without PMP for now, it should succeed but might be logically invalid for AMP).
- How does the system handle simultaneous UART output from 4 cores? (Should be handled by gem5's terminal support or multiplexing).

## Requirements

### Functional Requirements

- **FR-001**: The system MUST be configured with 4 RISC-V 32-bit CPU cores.
- **FR-002**: The system MUST provide 1MB of SRAM for *each* core (Total 4MB SRAM).
- **FR-003**: The system MUST provide 2MB of MRAM for *each* core (Total 8MB MRAM).
- **FR-004**: The memory map MUST define distinct non-overlapping regions for each core's SRAM and MRAM starting at MRAM Base 0x30000000 and SRAM Base 0x40000000.
- **FR-005**: The system MUST support loading and executing Zephyr OS on all 4 cores simultaneously in AMP mode.
- **FR-006**: The simulation configuration MUST allow specifying 4 separate Zephyr kernel binaries using gem5's `Workload` object, one for each core.
- **FR-007**: The system MUST provide 4 separate UART devices, one dedicated to each core, mapped to distinct IO addresses and terminals.

### Assumptions

- The "previously created RISC-V 32-bit core" refers to the `Riscv32` CPU type used in prior configurations.
- Zephyr OS images will be provided or built separately; this feature focuses on the gem5 hardware configuration and ensuring it *can* run them.
- A single UART or multiple UARTs will be used for output; standard practice for simple AMP is often one UART per core or a shared one with locking, but for simulation, multiple UARTs or a mux is preferred. I will assume the existing UART setup needs to be scaled or managed.
- MRAM is modeled as a memory controller with specific latency/characteristics as per previous tasks (STT-MRAM).

### Key Entities

- **QuadCoreSystem**: The top-level gem5 system object containing 4 CPU clusters/cores.
- **CoreMemory**: The dedicated memory pair (SRAM+MRAM) for each core.

## Success Criteria

### Measurable Outcomes

- **SC-001**: Simulation successfully instantiates 4 CPU objects and their associated memory controllers.
- **SC-002**: Total system memory recognized matches 12MB (4x1MB SRAM + 4x2MB MRAM) plus any shared peripherals.
- **SC-003**: 4 instances of Zephyr OS reach the "Boot banner" or shell prompt in the simulation output.
