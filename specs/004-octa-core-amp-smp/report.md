# Phase 4 Completion Report: Octa-Core AMP/SMP (Dining Philosophers)

**Date:** 2025-12-03
**Status:** Completed
**Branch:** `004-octa-core-amp-smp`

## 1. Objective
The goal of Phase 4 was to verify the SMP capabilities of the Octa-Core RISC-V system by running a synchronization-heavy workload ("Dining Philosophers") on the SMP cluster (Cluster 1, Cores 4-7), while simultaneously maintaining independent AMP workloads on Cluster 0 (Cores 0-3).

## 2. Implementation Summary

### 2.1. Zephyr Application: `smp_philosophers`
- **Location:** `src/zephyr_apps/smp_philosophers`
- **Description:** Adapted Zephyr's standard `samples/philosophers` for the gem5 RISC-V SMP environment.
- **Configuration:**
    - Enabled SMP (`CONFIG_SMP=y`) with 4 cores (`CONFIG_MP_MAX_NUM_CPUS=4`).
    - Boot Hart set to 4 (`CONFIG_RV_BOOT_HART=4`) to align with Cluster 1's hardware ID.
    - **Overlay (`gem5_smp.overlay`)**:
        - Mapped Shared MRAM (Code) to `0x80000000` (Size increased to 64MB).
        - Mapped Shared SRAM (Data) to `0x90400000` (4MB).
        - Configured UART4 (`0x10014000`) as the console for the SMP cluster.

### 2.2. gem5 Configuration Updates
- **File:** `configs/riscv_rt/fs_octa_hybrid.py`
- **Change:** Increased MRAM size for Cluster 1 from 8MB to 64MB to accommodate the larger memory footprint of the SMP synchronization primitives and application code.

### 2.3. Build & Run Scripts
- **`build_smp_philosophers.sh`**: Automates the build process for the Dining Philosophers application using `west`.
- **`run_octa_philosophers.sh`**: Orchestrates the full simulation, loading:
    - Cores 0-3: `hello_world` (AMP, independent instances)
    - Cores 4-7: `smp_philosophers` (SMP, single kernel instance)

## 3. Verification Results

### 3.1. Simulation Execution
- **Command:** `./run_octa_philosophers.sh`
- **Duration:** Simulation ran successfully until manual termination.

### 3.2. Output Analysis
- **Cluster 0 (AMP Cores 0-3):**
    - Verified independent "Hello World" outputs on `system.platform.terminal` through `terminal3`.
    - Confirmed independent boot and execution.
- **Cluster 1 (SMP Cores 4-7):**
    - Verified "Dining Philosophers" output on `system.platform.terminal4`.
    - **Key Observation:** The output demonstrated active thread switching and resource sharing (forks) between multiple philosophers (representing simulated CPUs/threads) without deadlock.

    **Sample Output (Terminal 4):**
    ```text
    Philosopher 0 [P: 3]        STARVING         HOLDING ONE FORK    THINKING [  100 ms ] 
    Philosopher 1 [P: 2]  THINKING [  325 ms ] THINKING [  325 ms ]   EATING  [  225 ms ] 
    Philosopher 2 [P: 1]    DROPPED ONE FORK   THINKING [  225 ms ]   EATING  [  175 ms ]
    ```

## 4. Issues Resolved
1.  **Overlay UART Definitions:** Fixed undefined `uart0` references in AMP overlays by explicitly defining UART nodes in the `soc` block.
2.  **Memory Access Violation:** Resolved an out-of-bounds memory access error `0x82028fc0` by increasing the simulated MRAM size for Cluster 1 to 64MB.
3.  **Duplicate Labels:** Fixed DTS syntax errors regarding duplicate `flash0` labels in overlays.

## 5. Conclusion
Phase 4 successfully demonstrated the hybrid architecture's capability to run heterogeneous workloads simultaneously. The SMP cluster correctly handles shared memory and synchronization primitives required for multi-threaded OS execution, while the AMP cluster operates independently. The system is now ready for more complex inter-cluster communication scenarios (Phase 5).
