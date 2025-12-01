# Data Model: Octa-Core AMP/SMP

## 1. Memory Entities

### 1.1 Shared MRAM (Cluster 1 Code)
- **Base Address**: `0x80000000` (or distinct region if needed, e.g., `0xA0000000`)
- **Size**: 8 MB
- **Access**: Shared R/W/X by Cores 4-7
- **Latency**: Asymmetric (Read: 20ns, Write: 100ns)

### 1.2 Shared SRAM (Cluster 1 Data)
- **Base Address**: `0x90400000` (Following Core 3's SRAM at `0x90300000`)
- **Size**: 4 MB
- **Access**: Shared R/W by Cores 4-7
- **Latency**: Symmetric (1 cycle)

### 1.3 Dedicated SRAMs (Cluster 0)
- **Core 0**: `0x90000000` (1MB)
- **Core 1**: `0x90100000` (1MB)
- **Core 2**: `0x90200000` (1MB)
- **Core 3**: `0x90300000` (1MB)

## 2. IO Entities

### 2.1 UARTs
- **UART0**: `0x10010000` (Core 0)
- **UART1**: `0x10011000` (Core 1)
- **UART2**: `0x10012000` (Core 2)
- **UART3**: `0x10013000` (Core 3)
- **UART4**: `0x10014000` (Cluster 1 Shared)

## 3. CPU Entities

### 3.1 Cluster 0 (AMP)
- **Cores**: 0-3
- **Type**: RV32IMAC
- **OS**: Zephyr (Independent Instances)

### 3.2 Cluster 1 (SMP)
- **Cores**: 4-7
- **Type**: RV32IMAC
- **OS**: Zephyr (Single SMP Instance)
- **Coherency**: Hardware-managed via CoherentXBar
