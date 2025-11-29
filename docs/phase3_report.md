# Phase 3 Completion Report: Quad-Core AMP Implementation

## 1. Executive Summary
Phase 3 of the project has been successfully completed. We have implemented and verified a Quad-Core Asymmetric Multi-Processing (AMP) system on gem5 using the RISC-V architecture. Each of the four cores runs an independent instance of the Zephyr RTOS, communicating via dedicated UARTs.

## 2. Key Achievements
- **Quad-Core Platform**: Extended the `HiFive` platform in gem5 to support 4 cores and 4 independent UARTs.
- **Custom Bootloader**: Developed a multi-core bootloader (`boot.S`) that dispatches each core to its specific kernel entry point based on `mhartid`.
- **Zephyr Integration**: Configured Zephyr to support the custom memory map and interrupt routing for each core.
- **Interrupt Routing**: Successfully patched gem5's `Uart8250` model to support custom interrupt IDs, enabling independent console output for each core.
- **Stability**: Resolved memory map crashes by implementing "Ghost Memory" regions to handle stray accesses during boot.

## 3. Technical Implementation Details

### 3.1 gem5 Configuration
- **Platform**: `QuadHiFive` (extends `HiFive`)
- **UARTs**:
    - UART0: `0x10010000` (IRQ 10) -> Core 0
    - UART1: `0x10011000` (IRQ 11) -> Core 1
    - UART2: `0x10012000` (IRQ 12) -> Core 2
    - UART3: `0x10013000` (IRQ 13) -> Core 3
- **Memory Map**:
    - Core 0 SRAM: `0x90000000`
    - Core 1 SRAM: `0x90100000`
    - Core 2 SRAM: `0x90200000`
    - Core 3 SRAM: `0x90300000`

### 3.2 Bootloader
The bootloader resides at `0x80000000` (Reset Vector). It performs the following:
1.  Reads the `mhartid` CSR (`0xf14`).
2.  Calculates the target kernel address: `0x90000000 + (mhartid * 1MB)`.
3.  Jumps to the target address.

### 3.3 Zephyr Configuration
Each core runs a separate Zephyr binary built with:
- **Board**: `hifive1`
- **DTS Overlay**: Custom overlay mapping the specific UART and interrupt.
- **Boot Hart**: `CONFIG_RV_BOOT_HART` set to the core's ID to ensure it boots as the primary hart.

## 4. Verification Results
The system was verified by running a full-system simulation:
```bash
src/gem5/build/RISCV/gem5.opt configs/riscv_rt/fs_quad_amp.py \
    --kernels src/zephyr_apps/hello_world/build_core0/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core1/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core2/zephyr/zephyr.elf,src/zephyr_apps/hello_world/build_core3/zephyr/zephyr.elf \
    --bootloader src/bootloader/bootloader.elf
```

All four cores successfully booted and printed "Hello World" to their respective terminals:
- Core 0: `m5out/system.platform.terminal`
- Core 1: `m5out/system.platform.terminal1`
- Core 2: `m5out/system.platform.terminal2`
- Core 3: `m5out/system.platform.terminal3`

## 5. Next Steps
- **Phase 4**: Inter-Core Communication (ICC) using Shared Memory.
- **Performance Analysis**: Measure latency and throughput of the AMP system.
