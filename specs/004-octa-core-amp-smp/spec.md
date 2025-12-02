# Feature Specification: Octa-Core AMP/SMP Cluster Configuration

## 1. Introduction
This feature expands the existing Quad-Core AMP system into an Octa-Core (8-core) heterogeneous system. It introduces a second cluster (Cluster 1) configured for Symmetric Multi-Processing (SMP) with cache coherency, running a single instance of Zephyr RTOS. The system will demonstrate a hybrid AMP/SMP architecture where Cluster 0 continues to operate in AMP mode, while Cluster 1 handles compute-intensive SMP workloads like PARSEC.

## 2. Clarifications
### Session 2025-11-29
- Q: UART Configuration for SMP Cluster? → A: Single Shared UART (UART4) for all SMP cores.
- Q: Bootloader Behavior for SMP Secondary Cores? → A: Park in WFI; Primary core wakes them.

## 3. User Scenarios
- **Scenario 1: Hybrid Workload Execution**
    - **User** boots the simulation.
    - **System** starts 4 independent Zephyr kernels on Cluster 0 (Cores 0-3) and 1 SMP Zephyr kernel on Cluster 1 (Cores 4-7).
    - **Cluster 0** executes real-time/independent tasks (e.g., "Hello World").
    - **Cluster 1** executes a multi-threaded SMP workload (e.g., PARSEC benchmark).
    - **User** verifies output from all 5 contexts (4 AMP + 1 SMP Shared Console).

- **Scenario 2: SMP Performance Analysis**
    - **User** runs the SMP Synchronization Sample on Cluster 1.
    - **System** utilizes all 4 cores in Cluster 1 with cache coherency.
    - **User** observes successful synchronization and data sharing across cores.

## 4. Functional Requirements

### 4.1 System Architecture
- **Total Cores**: 8 x RISC-V (RV32IMAC) Cores.
- **Cluster Configuration**:
    - **Cluster 0 (AMP)**: Cores 0-3. Shared L2 Cache (Cluster 0). Independent execution.
    - **Cluster 1 (SMP)**: Cores 4-7. Shared L2 Cache (Cluster 1). Cache Coherent.

### 4.2 Memory Subsystem
- **Cluster 1 Memory**:
    - **MRAM (Code)**: 8 MB Total (Logically shared).
    - **SRAM (Data)**: 4 MB Total (Logically shared).
    - **Mapping**: Contiguous addressing for SMP OS visibility.

### 4.3 IO Subsystem
- **Cluster 0 (AMP)**: 4 Dedicated UARTs (UART0-3), one per core.
- **Cluster 1 (SMP)**: 1 Shared UART (UART4) for Cores 4-7.

### 4.4 Software Configuration
- **Cluster 0**: Existing independent Zephyr kernels (AMP).
- **Cluster 1**: Single Zephyr SMP kernel managing Cores 4-7.
- **Bootloader**:
    - **Core 0-3**: Jump to respective kernel entry.
    - **Core 4 (SMP Primary)**: Jump to SMP kernel entry.
    - **Core 5-7 (SMP Secondary)**: Park in `wfi` loop, waiting for wake-up signal (IPI/HSM).
- **Workloads**:
    - **Basic**: "Hello World" on all contexts.
    - **Verification**: Zephyr SMP Synchronization Sample (`samples/synchronization`) on Cluster 1.
    - **Advanced (Future)**: PARSEC benchmark (or equivalent multi-threaded workload) on Cluster 1.

### 4.5 Simulation Platform
- **Configuration**: Extend the simulation platform to support 8 cores arranged in 2 clusters.
- **Coherency**: Ensure the memory model supports cache coherency within Cluster 1 (SMP).

## 5. Success Criteria
- **Boot Success**: All 8 cores boot successfully.
- **Output Verification**:
    - Cores 0-3 print independent "Hello World" messages to UART0-3.
    - Cluster 1 (SMP) prints unified boot message and workload output to UART4.
- **Workload Execution**: PARSEC benchmark runs to completion on Cluster 1 without coherency errors.
- **Architecture Validation**: `config.dot` or `m5out` stats confirm the 2-cluster topology and cache hierarchy.

## 6. Assumptions & Constraints
- **PARSEC Availability**: Assumes a Zephyr-compatible port of a PARSEC benchmark (e.g., `blackscholes` or `canneal`) or a similar multi-threaded stress test is available or can be easily adapted.
- **Memory Model**: Classic memory system will be used for simplicity unless Ruby is strictly required for the specific coherency protocol desired (Classic snooping should suffice for SMP).
- **Zephyr SMP**: Zephyr's SMP support for RISC-V is assumed to be stable enough for this simulation.

## 7. Workload Details
- **Cluster 1 Workload**: Zephyr's built-in SMP synchronization sample (`samples/synchronization`) or a similar synthetic stress test will be used.
    - **Reasoning**: This provides a reliable, low-risk method to verify cache coherency and multicore scheduling on the new SMP cluster without the complexity of porting full Linux benchmarks.
    - **Verification**: The test must demonstrate successful locking/unlocking and data sharing across all 4 cores in Cluster 1.
