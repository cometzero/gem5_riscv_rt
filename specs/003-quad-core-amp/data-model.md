# System Architecture: Quad Core AMP

**Feature**: Quad Core AMP Zephyr
**Status**: Draft

## Entities

### 1. QuadCoreSystem
The top-level system container.
- **Attributes**:
  - `cpu`: List[TimingSimpleCPU] (Size: 4)
  - `mem_mode`: "timing"
  - `mem_ranges`: List[AddrRange] (Aggregated ranges)
  - `workload`: RiscvBareMetal (or list thereof)

### 2. CoreCluster
Logical grouping of a Core and its dedicated resources.
- **Attributes**:
  - `core_id`: Integer (0-3)
  - `cpu`: TimingSimpleCPU
  - `sram`: SimpleMemory (1MB)
  - `mram`: MemCtrl + STTMRAM (2MB)
  - `uart`: RiscvUart

### 3. MemoryMap
Global address map for the AMP system.

| Region | Start Addr | Size | Owner |
|--------|------------|------|-------|
| Boot ROM | 0x00000000 | 64KB | Shared |
| MRAM 0 | 0x30000000 | 2MB | Core 0 |
| MRAM 1 | 0x30200000 | 2MB | Core 1 |
| MRAM 2 | 0x30400000 | 2MB | Core 2 |
| MRAM 3 | 0x30600000 | 2MB | Core 3 |
| SRAM 0 | 0x40000000 | 1MB | Core 0 |
| SRAM 1 | 0x40100000 | 1MB | Core 1 |
| SRAM 2 | 0x40200000 | 1MB | Core 2 |
| SRAM 3 | 0x40300000 | 1MB | Core 3 |
| UART 0 | 0x10010000 | 4KB | Core 0 |
| UART 1 | 0x10011000 | 4KB | Core 1 |
| UART 2 | 0x10012000 | 4KB | Core 2 |
| UART 3 | 0x10013000 | 4KB | Core 3 |

## Relationships

- `QuadCoreSystem` contains 4 `CoreCluster` instances (logically).
- Each `CoreCluster` owns 1 `SRAM` and 1 `MRAM` region.
- Each `CoreCluster` is associated with 1 `UART`.
