# Feature Specification: Phase 2 Memory Architecture Exploration

## 1. Overview

**Feature Name**: Phase 2 Memory Architecture Exploration
**Version**: 1.0
**Status**: Draft
**Last Updated**: 2025-11-25

### Executive Summary

This phase expands the gem5 RISC-V simulation framework to support advanced memory architectures. It introduces SRAM, NOR Flash, and STT-MRAM models using the Ruby memory system, enabling the exploration of heterogeneous memory hierarchies. The goal is to validate mixed-memory workloads (e.g., critical code in SRAM, bulk data in DRAM/MRAM) and analyze performance, latency, and energy characteristics for automotive real-time systems.

## Clarifications

### Session 2025-11-25
- **Q: Flash Boot Mechanism?** → **A: XIP (Execute-In-Place)**. The NOR Flash will be modeled as a ROM-like memory mapped at `0x20000000`, allowing Zephyr to execute code directly from Flash (XIP) or copy it to SRAM.
- **Q: Ruby Coherence Protocol?** → **A: MI_example**. We will use the `MI_example` protocol as it is simpler and sufficient for the embedded, single-core (or small multi-core) nature of this project, avoiding the complexity of hierarchical protocols like MESI_Two_Level.
- **Q: STT-MRAM Default Latency?** → **A: Read 10ns / Write 50ns**. Default timing parameters will be set to these typical values for STT-MRAM to ensure asymmetric latency modeling is verifiable.

### Context & Goals

**Problem Statement**:
Phase 1 established a baseline with a simple DRAM-only memory system. However, real automotive systems utilize complex memory hierarchies including SRAM (for critical tasks), NOR Flash (for boot), and emerging NVMs like STT-MRAM. The current baseline cannot simulate these heterogeneous configurations or their impact on real-time performance.

**Goals**:
1.  **Advanced Memory Modeling**: Implement SRAM, NOR Flash, and STT-MRAM using gem5's Ruby memory system.
2.  **Heterogeneous Boot**: Support booting from SRAM (code execution) with Flash storage models.
3.  **Mixed Workloads**: Define and validate workloads that utilize both SRAM and DRAM/MRAM.
4.  **Design Space Exploration**: Enable configuration of memory hierarchies to analyze trade-offs in latency, bandwidth, and performance.

### Out of Scope
- Detailed circuit-level power modeling (approximate energy models are sufficient).
- Complex automotive bus protocols (CAN/LIN) simulation (focus is on memory bus).
- Full OS file system support for Flash (simple raw access or block device model is sufficient).

## 2. User Scenarios

### Scenario 1: SRAM-based Critical Boot
**Actor**: Automotive System Architect
**Action**: Configures the simulation to boot Zephyr directly from a 2MB SRAM region.
**Outcome**: The system boots faster than DRAM-only configurations due to lower latency, and critical initialization code executes deterministically.

### Scenario 2: Mixed Criticality Workload Execution
**Actor**: Real-Time Software Engineer
**Action**: Runs an automotive control loop where the control task code and data reside in SRAM, while logging/monitoring data resides in DRAM.
**Outcome**: The critical control task shows reduced execution time variance and lower latency compared to running entirely in DRAM, even when DRAM is under load from background tasks.

### Scenario 3: STT-MRAM Evaluation
**Actor**: Hardware Researcher
**Action**: Replaces DRAM with STT-MRAM in the simulation configuration and runs the standard workload.
**Outcome**: The simulation provides metrics on write latency impact, endurance (write counts), and potential energy savings, allowing comparison with DRAM baseline.

### Edge Cases

- **SRAM Overflow**: If the Zephyr kernel + critical application code exceeds the 2MB SRAM limit, the linker or loader must fail gracefully with a clear error message.
- **Invalid Memory Config**: If a user selects an incompatible combination (e.g., "SRAM boot" without defining SRAM region), the simulation script should abort before starting gem5.
- **Boot Failure**: If Flash-to-SRAM copy fails (e.g., due to simulated corruption or address error), the system should halt or trigger a simulated watchdog reset.
- **Address Overlap**: Ensure that the memory map for SRAM, DRAM, and Flash does not overlap to prevent undefined behavior in the Ruby memory system.

## 3. Functional Requirements

### 3.1 Advanced Memory Modeling & Ruby SRAM (RUBY/SRAM2)

| ID | Requirement | Priority |
|----|-------------|----------|
| RUBY-001 | Define a Ruby memory system configuration that supports heterogeneous memory types (SRAM, DRAM, STT-MRAM) within a single coherent address space. | High |
| RUBY-002 | Provide configuration options to switch between Classic Memory system (Phase 1 baseline) and Ruby Memory system. | High |
| SRAM2-001 | Implement a 2MB SRAM memory region in the memory map, distinct from main DRAM. | High |
| SRAM2-002 | Configure Zephyr to link critical code/data sections to the SRAM address range. | High |
| SRAM2-003 | Model SRAM latency and bandwidth characteristics distinct from DRAM (e.g., 1-cycle access). | Medium |

### 3.2 Mixed SRAM + DRAM Workload (MIX)

| ID | Requirement | Priority |
|----|-------------|----------|
| MIX-001 | Define a workload strategy where critical control tasks are placed in SRAM and background tasks in DRAM. | High |
| MIX-002 | Provide linker scripts or Zephyr configuration to support `.text_sram` and `.data_sram` sections. | High |
| MIX-003 | Create an interference scenario where background DRAM traffic attempts to impact system performance, validating SRAM isolation. | Medium |
| MIX-004 | Define two workload scenarios: (A) SRAM-dominant (most code in SRAM), (B) Mixed (only critical path in SRAM). | Medium |
| MIX-005 | Collect metrics on SRAM vs. DRAM access ratios and latency distributions per memory type. | High |

### 3.3 NOR Flash Modeling (FLASH2)

| ID | Requirement | Priority |
|----|-------------|----------|
| FLASH2-001 | Model a NOR Flash device with specific address range, read latency, and throughput constraints. | Medium |
| FLASH2-002 | Support a boot flow where code is copied from Flash to SRAM/DRAM (XIP-like behavior or bootloader copy). | Medium |
| FLASH2-003 | Integrate Flash model into the gem5 configuration and ensure visibility to Zephyr. | Medium |

### 3.4 STT-MRAM Modeling (STTM)

| ID | Requirement | Priority |
|----|-------------|----------|
| STTM-001 | Implement an STT-MRAM memory model (e.g., using NVMain or Ruby configuration) with asymmetric read/write latencies. | High |
| STTM-002 | Support three configurations: (a) DRAM-only, (b) STT-MRAM-only, (c) Hybrid (DRAM + STT-MRAM). | High |
| STTM-003 | Provide a unified configuration interface to select the memory technology for main memory. | Medium |
| STTM-004 | Ensure compatibility of STT-MRAM configurations with SRAM boot and Zephyr workloads. | High |
| STTM-005 | Collect specific NVM metrics: write counts, write energy (estimated), and read/write latency breakdown. | Medium |

### 3.5 Experiment & Results (EXP2)

| ID | Requirement | Priority |
|----|-------------|----------|
| EXP2-001 | Define standard configurations for comparison: CFG-A (SRAM+DRAM), CFG-B (SRAM+MRAM), CFG-C (Hybrid). | High |
| EXP2-002 | Execute baseline automotive workload and a memory-stress workload on all standard configurations. | High |
| EXP2-003 | Extend the metrics pipeline to report memory-type specific statistics (SRAM hits, MRAM writes, etc.). | High |
| EXP2-004 | Generate a comparative report (Phase 2 Report) analyzing the trade-offs between configurations. | High |

### 3.6 Traceability (TRC2)

| ID | Requirement | Priority |
|----|-------------|----------|
| TRC2-001 | Maintain backward compatibility with Phase 1 baseline (Classic Memory, DRAM-only) via configuration switches. | High |
| TRC2-002 | Map Phase 2 components to Phase 1 architecture to ensure architectural consistency. | Low |

## 4. Success Criteria

### Quantitative Metrics
1.  **SRAM Boot**: Zephyr boots successfully from the defined 2MB SRAM address range.
2.  **Latency Differentiation**: SRAM access latency is consistently lower than DRAM/MRAM in simulation stats.
3.  **STT-MRAM Characteristics**: Write operations to STT-MRAM show higher latency than reads (asymmetric modeling verified).
4.  **Workload Isolation**: Critical tasks in SRAM show < 5% execution time variance even with heavy DRAM background traffic.
5.  **Pipeline Automation**: `run_sim.sh` and `postprocess.py` support new configurations and generate extended CSV reports.

### Qualitative Metrics
1.  **Configurability**: Users can switch between memory models (Classic vs. Ruby) and technologies (DRAM vs. MRAM) via command-line arguments.
2.  **Report Quality**: Phase 2 report clearly visualizes the trade-offs (e.g., "SRAM reduces latency by X%", "MRAM increases write latency by Y%").

## 5. Assumptions & Dependencies

### Assumptions
- **Ruby Support**: gem5's Ruby system supports the RISC-V architecture sufficiently for this level of modeling.
- **Zephyr Relocation**: Zephyr RTOS supports relocation of text/data sections via standard Kconfig/linker scripts without kernel modifications.
- **Energy Models**: Simple energy models (pJ per access) are sufficient; cycle-accurate power gating is not required.

### Dependencies
- **Phase 1 Completion**: Requires the functional Zephyr port and baseline simulation environment (Completed).
- **gem5 Ruby**: Requires compilation of gem5 with Ruby protocol support (likely `MI_example` or `MESI_Two_Level`).

## 6. Data Requirements

- **Memory Parameters**: Datasheet values for SRAM, DDR3 DRAM, and STT-MRAM (latency, bandwidth, energy) to configure the models.
- **Workload Profiles**: Memory access patterns of the automotive workload to define "critical" vs "non-critical" data.
