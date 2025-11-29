# Quad-Core AMP System Architecture

This document visualizes the hardware architecture simulated in Phase 3. The system is a Quad-Core RISC-V SoC designed for Asymmetric Multi-Processing (AMP) with independent IO for each core.

## Block Diagram

```mermaid
graph TD
    subgraph CPU_Complex [CPU Complex]
        direction TB
        C0[Core 0<br/>RV32IMAC]
        C1[Core 1<br/>RV32IMAC]
        C2[Core 2<br/>RV32IMAC]
        C3[Core 3<br/>RV32IMAC]
    end

    subgraph Interrupts [Interrupt Controllers]
        CLINT[CLINT<br/>Timer/Soft Int]
        PLIC[PLIC<br/>External Int]
    end

    subgraph Interconnect [System Interconnect]
        MB[System MemBus<br/>Crossbar]
        IOB[IO Bus<br/>Crossbar]
    end

    subgraph Memory [Memory Subsystem]
        ROM[Boot ROM<br/>0x0000_0000]
        Flash[NOR Flash<br/>0x2000_0000]
        
        subgraph SRAMs [Dedicated SRAMs]
            S0[SRAM 0<br/>0x9000_0000]
            S1[SRAM 1<br/>0x9010_0000]
            S2[SRAM 2<br/>0x9020_0000]
            S3[SRAM 3<br/>0x9030_0000]
        end
        
        MRAM[Main Memory<br/>MRAM/DRAM<br/>0x8000_0000]
    end

    subgraph IO [Peripherals]
        U0[UART 0<br/>0x1001_0000<br/>IRQ 10]
        U1[UART 1<br/>0x1001_1000<br/>IRQ 11]
        U2[UART 2<br/>0x1001_2000<br/>IRQ 12]
        U3[UART 3<br/>0x1001_3000<br/>IRQ 13]
    end

    %% CPU to Bus Connections
    C0 <--> MB
    C1 <--> MB
    C2 <--> MB
    C3 <--> MB

    %% Bus to Memory Connections
    MB <--> ROM
    MB <--> Flash
    MB <--> S0
    MB <--> S1
    MB <--> S2
    MB <--> S3
    MB <--> MRAM

    %% Bus to IO Connections
    MB <--> IOB
    IOB <--> U0
    IOB <--> U1
    IOB <--> U2
    IOB <--> U3
    IOB <--> CLINT
    IOB <--> PLIC

    %% Interrupt Routing
    U0 -.->|IRQ 10| PLIC
    U1 -.->|IRQ 11| PLIC
    U2 -.->|IRQ 12| PLIC
    U3 -.->|IRQ 13| PLIC

    PLIC == External Int ==> C0
    PLIC == External Int ==> C1
    PLIC == External Int ==> C2
    PLIC == External Int ==> C3

    CLINT == Timer/Soft Int ==> C0
    CLINT == Timer/Soft Int ==> C1
    CLINT == Timer/Soft Int ==> C2
    CLINT == Timer/Soft Int ==> C3
```

## Memory Map

| Region | Start Address | Size | Description |
| :--- | :--- | :--- | :--- |
| **Boot ROM** | `0x0000_0000` | 64 KB | Holds the Bootloader (`boot.S`) |
| **UART 0** | `0x1001_0000` | 4 KB | Console for Core 0 |
| **UART 1** | `0x1001_1000` | 4 KB | Console for Core 1 |
| **UART 2** | `0x1001_2000` | 4 KB | Console for Core 2 |
| **UART 3** | `0x1001_3000` | 4 KB | Console for Core 3 |
| **Flash** | `0x2000_0000` | 32 MB | XIP Storage (Unused in RAM boot) |
| **Main Mem** | `0x8000_0000` | 128 MB | Shared DRAM/MRAM |
| **SRAM 0** | `0x9000_0000` | 1 MB | Dedicated RAM for Core 0 Kernel |
| **SRAM 1** | `0x9010_0000` | 1 MB | Dedicated RAM for Core 1 Kernel |
| **SRAM 2** | `0x9020_0000` | 1 MB | Dedicated RAM for Core 2 Kernel |
| **SRAM 3** | `0x9030_0000` | 1 MB | Dedicated RAM for Core 3 Kernel |

## Interrupt Routing

| Peripheral | Interrupt ID | Target Core |
| :--- | :--- | :--- |
| **UART 0** | 10 | Core 0 |
| **UART 1** | 11 | Core 1 |
| **UART 2** | 12 | Core 2 |
| **UART 3** | 13 | Core 3 |

Each core is configured in Zephyr to listen to its specific UART interrupt line via the PLIC.
