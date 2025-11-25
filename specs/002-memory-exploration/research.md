# Research: Phase 2 Memory Architecture Exploration

## 1. Memory System: Ruby vs. Classic

**Context**: The requirement mentions using "Ruby memory system etc." to model SRAM/DRAM/NVM. We need to decide whether to strictly use Ruby or if Classic Memory is more suitable for this embedded RISC-V context.

### Analysis
- **Ruby**:
  - **Pros**: Detailed coherence modeling, advanced network topologies (Mesh, Crossbar), supports `MemoryControl` with detailed timing.
  - **Cons**: High complexity, typically designed for uniform main memory. Mapping disjoint address ranges (SRAM @ 0x80000000, DRAM @ 0xA0000000) to different controllers requires specific config hacking (e.g., `Directory_Controller` ranges).
  - **RISC-V Support**: Supported, but less tested with heterogeneous setups than ARM/X86.
- **Classic**:
  - **Pros**: Native support for heterogeneous memory maps (XBar routing based on address ranges). Easy to mix `SimpleMemory` (SRAM), `DRAMCtrl` (DRAM), and `NVMInterface` (MRAM).
  - **Cons**: Less detailed coherence traffic modeling (though `CoherentXBar` is decent).

### Decision
**Use Classic Memory System for primary exploration, but provide a Ruby configuration for advanced coherence studies.**
- **Rationale**: The primary goal is "Memory Architecture Exploration" (latency, bandwidth, mixing types). Classic Memory's `HeterogeneousMemory` support is robust and fits the Zephyr/Embedded use case perfectly (System-on-Chip style). Ruby adds unnecessary complexity for a single-core (or small multi-core) embedded system unless we are specifically studying coherence protocols.
- **Note**: The spec asked for "Ruby... etc". We will interpret this as "Advanced modeling". We will implement the Classic model first (as it guarantees functionality) and attempt a Ruby config as an advanced option if time permits, or justify why Classic is sufficient for the "latency/energy" goals.
- **Update**: Re-reading the spec, `RUBY-001` explicitly requires Ruby. We will proceed with **Ruby** as the primary requirement, using `MI_example` protocol (simple 1-level coherence) and mapping different address ranges to different Directory controllers backed by different memory configurations.

## 2. Zephyr SRAM Boot Strategy

**Context**: Booting Zephyr from SRAM instead of Flash/DRAM.

### Analysis
- **Standard Boot**: Zephyr links to `CONFIG_FLASH_BASE_ADDRESS`.
- **SRAM Boot**:
  - Option A: Change `CONFIG_FLASH_BASE_ADDRESS` to SRAM address in Kconfig.
  - Option B: Use `zephyr,sram` as the boot source in DTS `chosen` node.
  - Option C: Use a "RAM loadable" image configuration.

### Decision
**Option A + B (DTS & Kconfig modification)**.
- **Rationale**: We will define a new `gem5_riscv32_sram` board variant (or overlay) that redefines the memory map.
- **Memory Map**:
  - SRAM: `0x80000000` (2MB) - Mapped to `zephyr,flash` for XIP.
  - DRAM: `0x80200000` (126MB) - Mapped to `zephyr,sram` for data.
  - (Note: gem5's default memory starts at 0x80000000. We will split this range).

## 3. STT-MRAM Modeling

**Context**: Modeling STT-MRAM latency and energy.

### Analysis
- **gem5 Support**: `NVMInterface` in `src/mem/NVMInterface.py` supports PCM-like characteristics (asymmetric R/W).
- **Integration**:
  - Classic: Direct use of `NVMInterface`.
  - Ruby: `RubyMemoryControl` can interface with `NVMInterface` (if supported in v25.0) or we use generic `MemoryControl` with custom latency parameters.

### Decision
**Use `NVMInterface` (Classic) or parameterized `MemoryControl` (Ruby).**
- **Rationale**: If using Ruby, we will configure the `Directory_Controller` for the MRAM range to use a `MemoryControl` with timings matching STT-MRAM (e.g., longer write latency).

## 4. Mixed Workload Strategy

**Context**: Placing critical code in SRAM.

### Decision
**Use Zephyr Linker Sections.**
- Define `__attribute__((section(".sram_text")))` macros.
- Update linker script to map `.sram_text` to the SRAM region.
- This allows fine-grained control over which functions reside in SRAM.
