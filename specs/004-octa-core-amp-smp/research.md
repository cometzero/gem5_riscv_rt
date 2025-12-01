# Research: Octa-Core AMP/SMP

## 1. gem5 Classic Memory Model Coherency
**Question**: Does the Classic memory model support snooping/coherency out-of-the-box for the SMP cluster?
**Findings**:
- The Classic memory system in gem5 uses a snooping protocol by default when caches are connected to a shared bus (`SystemXBar` or `L2XBar`).
- `CoherentXBar` is the standard crossbar used for coherency.
- In `fs_quad_amp.py`, we use `SystemXBar` (which inherits from `CoherentXBar`).
- **Decision**: We will use the existing Classic memory model. We need to ensure that the L2 cache for Cluster 1 is connected to a `CoherentXBar` that all 4 SMP cores (Cores 4-7) share. This will automatically handle snooping and coherency.
- **Rationale**: Classic model is simpler and sufficient for this use case. Ruby is overkill unless we need specific protocol modeling.

## 2. Zephyr SMP Boot on RISC-V
**Question**: How does Zephyr handle secondary core boot on RISC-V?
**Findings**:
- Zephyr's RISC-V SMP implementation typically relies on the bootloader to park secondary harts.
- The primary hart (Boot Hart) initializes the kernel.
- The kernel then wakes up secondary harts using a platform-specific mechanism (often IPI or a shared memory flag if hardware support is limited).
- **Decision**: Our custom bootloader (`boot.S`) will park Cores 5-7 in a `wfi` loop. Core 4 will jump to the kernel.
- **Rationale**: This aligns with the clarification provided in the spec and standard RISC-V SMP boot flow.

## 3. gem5 Octa-Core Platform
**Question**: How to extend `QuadHiFive` to 8 cores?
**Findings**:
- `QuadHiFive.py` currently defines `uart1-3`.
- We need to define `uart4` for the SMP cluster.
- We need to define 4 additional CPU contexts in `fs_octa_hybrid.py`.
- We need to define the memory map for the new cluster (shared MRAM/SRAM).
- **Decision**: Create `OctaHiFive` platform inheriting from `HiFive` (or `QuadHiFive`). Add `uart4`.
- **Rationale**: Modular extension of existing platform code.
