# Feature Specification: gem5 RISC-V Full-System Simulation Framework

**Feature Branch**: `001-fullsystem-simulation`  
**Created**: 2025-11-23  
**Status**: Draft  
**Input**: User description: "gem5를 활용하여 RISC-V 32-bit in-order CPU + 캐시/메모리 계층 + NOR Flash를 포함한 full-system 시뮬레이션을 수행하고, Zephyr RTOS 기반의 automotive workload를 구동하여 설계 공간 탐색(DSE)을 수행한다."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Baseline Full-System Simulation (Priority: P1)

As a hardware architect, I need to run a baseline RISC-V 32-bit full-system simulation with Zephyr RTOS to establish a working reference configuration before exploring design alternatives.

**Why this priority**: Without a working baseline, no design space exploration can occur. This is the foundation for all subsequent experiments.

**Independent Test**: Can be fully tested by running a single gem5 simulation with the baseline configuration, booting Zephyr RTOS, executing a simple workload, and collecting basic performance statistics (IPC, execution time).

**Acceptance Scenarios**:

1. **Given** a clean repository clone, **When** I execute the baseline build and simulation script, **Then** gem5 boots Zephyr RTOS successfully and completes a simple workload
2. **Given** a completed baseline simulation, **When** I examine the output statistics, **Then** I can see IPC, cache miss rates, and memory access latency metrics
3. **Given** baseline configuration parameters, **When** I review the documentation, **Then** all CPU, cache, and memory parameters are clearly documented with their values

---

### User Story 2 - Cache Configuration Sweep (Priority: P2)

As a hardware architect, I need to sweep cache parameters (size, associativity, line size) while running the same workload to understand cache sensitivity and identify optimal configurations.

**Why this priority**: Cache configuration significantly impacts real-time performance and is a primary design variable in automotive systems.

**Independent Test**: Can be tested by running multiple simulations with different cache configurations (e.g., L1 size: 16KB, 32KB, 64KB) and comparing cache miss rates and performance metrics across configurations.

**Acceptance Scenarios**:

1. **Given** a baseline configuration, **When** I modify L1 cache size via script parameters, **Then** the simulation runs with the new cache configuration
2. **Given** multiple cache configurations, **When** I execute the sweep script, **Then** all simulations complete and results are collected in a structured format (CSV/JSON)
3. **Given** collected cache sweep results, **When** I compare configurations, **Then** I can identify which cache parameters most impact performance for the automotive workload

---

### User Story 3 - Memory Technology Comparison (Priority: P3)

As a hardware architect, I need to compare different memory technologies (SRAM, DRAM, STT-MRAM) to evaluate trade-offs between performance, latency, and energy for automotive applications.

**Why this priority**: Memory technology selection impacts both performance and power consumption, critical for automotive embedded systems.

**Independent Test**: Can be tested by running the same workload with DRAM-only, STT-MRAM-only, and hybrid configurations, then comparing memory access latency distributions and performance metrics.

**Acceptance Scenarios**:

1. **Given** a baseline DRAM configuration, **When** I switch to STT-MRAM via configuration parameter, **Then** the simulation runs with STT-MRAM memory model
2. **Given** multiple memory technology runs, **When** I compare results, **Then** I can see differences in average/maximum memory latency and overall performance
3. **Given** memory technology comparison data, **When** I review energy estimates (if available), **Then** I can assess power-performance trade-offs

---

### User Story 4 - TCM/TIM Configuration Analysis (Priority: P4)

As a hardware architect, I need to evaluate the impact of Tightly Coupled Memory (TCM) or Tightly Integrated Memory (TIM) on real-time workload predictability and performance.

**Why this priority**: TCM/TIM can significantly reduce worst-case execution time variability, important for automotive real-time guarantees.

**Independent Test**: Can be tested by running the same workload with TCM enabled vs disabled, comparing execution time variance and worst-case latency.

**Acceptance Scenarios**:

1. **Given** a baseline configuration without TCM, **When** I enable code/data TCM via configuration, **Then** the simulation maps specified code/data sections to TCM
2. **Given** TCM-enabled and TCM-disabled runs, **When** I compare execution time distributions, **Then** I can quantify the reduction in timing variability
3. **Given** TCM configuration parameters, **When** I modify TCM size, **Then** I can observe the impact on performance and memory access patterns

---

### User Story 5 - Automotive Workload Execution (Priority: P2)

As a hardware architect, I need to run automotive-representative workloads (periodic control loops, signal processing) on the simulated system to ensure realistic performance evaluation.

**Why this priority**: Generic benchmarks don't capture automotive-specific characteristics (periodicity, deadlines, interrupt patterns).

**Independent Test**: Can be tested by executing at least one automotive workload (e.g., periodic control loop with interrupt handling) and verifying that task deadlines are met and periodic behavior is maintained.

**Acceptance Scenarios**:

1. **Given** a Zephyr RTOS build with automotive workload, **When** I run the simulation, **Then** the workload executes with defined periodicity and completes within deadline
2. **Given** workload execution logs, **When** I analyze timing data, **Then** I can measure response time, jitter, and deadline miss rate
3. **Given** multiple workload types, **When** I switch between them via configuration, **Then** each workload runs successfully and produces comparable metrics

---

### Edge Cases

- What happens when cache size is set to zero (cache-less configuration)?
- How does the system handle memory configurations where total memory is insufficient to boot Zephyr?
- What happens when TCM size is larger than available physical memory?
- How does the simulation behave when workload execution time exceeds expected bounds?
- What happens when NOR Flash access latency is set to extreme values?
- How does the system handle concurrent cache/memory parameter sweeps (parameter space explosion)?

## Requirements *(mandatory)*

### Functional Requirements

#### System Overview (SYS-*)

- **SYS-001**: System MUST support RISC-V 32-bit (RV32IMAC or equivalent) in-order CPU simulation using gem5
- **SYS-002**: System MUST include configurable L1 instruction cache, L1 data cache, and L2 unified cache
- **SYS-003**: System MUST support at least three memory technology options: SRAM, DRAM, and STT-MRAM
- **SYS-004**: System MUST include NOR Flash storage model for boot code/image loading
- **SYS-005**: System MUST boot Zephyr RTOS in full-system simulation mode
- **SYS-006**: System MUST execute at least one automotive-representative workload successfully
- **SYS-007**: System MUST provide automated scripts for building and running simulations
- **SYS-008**: System MUST collect and export performance statistics (IPC, cache miss rates, memory latency) in structured format

#### CPU & ISA (CPU-*)

- **CPU-001**: gem5 configuration MUST use RV32 in-order CPU model with documented pipeline parameters
- **CPU-002**: CPU configuration MUST document branch predictor type, pipeline depth, and issue width
- **CPU-003**: System MUST define at least one baseline CPU configuration and one variant configuration (e.g., different branch predictor)
- **CPU-004**: CPU parameters MUST be configurable via script arguments or configuration files (not hardcoded)

#### Cache & TCM (CACHE-*, TCM-*)

- **CACHE-001**: L1/L2 cache parameters (size, associativity, line size, write policy) MUST be configurable via script parameters
- **CACHE-002**: System MUST collect cache statistics including miss rate, hit rate, and average access latency
- **CACHE-003**: Cache configurations MUST support parameter sweeps (e.g., L1 size: 16KB, 32KB, 64KB) via automated scripts
- **TCM-001**: System MUST support optional TCM/TIM configuration with configurable size and address mapping
- **TCM-002**: System MUST allow comparison between TCM-enabled and TCM-disabled configurations using the same workload
- **TCM-003**: TCM configuration MUST document code/data section mapping strategy

#### Memory & Storage (MEM-*, FLASH-*)

- **MEM-001**: System MUST support three memory configurations: DRAM-only, STT-MRAM-only, and hybrid DRAM+STT-MRAM
- **MEM-002**: Memory configuration MUST be selectable via script parameter
- **MEM-003**: System MUST collect memory access latency statistics (average, maximum, distribution)
- **MEM-004**: STT-MRAM simulation MUST use NVMain or equivalent memory model with documented latency/energy parameters
- **FLASH-001**: NOR Flash model MUST support boot code/image loading with configurable access latency
- **FLASH-002**: Boot sequence MUST successfully load Zephyr kernel from NOR Flash model

#### Software Stack (SW-*)

- **SW-001**: Zephyr RTOS MUST be buildable for RISC-V 32-bit target compatible with gem5 simulation
- **SW-002**: System MUST include at least one automotive workload (periodic control loop with interrupt handling)
- **SW-003**: System MUST include at least one microbenchmark (CoreMark or similar) for baseline performance measurement
- **SW-004**: Each workload MUST document real-time properties: period, deadline, priority
- **SW-005**: Workload selection MUST be configurable via script parameter

#### Experiment & Metrics (EXP-*)

- **EXP-001**: System MUST define at least three distinct configurations for comparison (e.g., TCM on/off, cache size variants, memory technology variants)
- **EXP-002**: Automated scripts MUST execute multiple configurations with the same workload and collect results
- **EXP-003**: Results MUST be exported in machine-readable format (CSV or JSON) with configuration parameters and metrics
- **EXP-004**: System MUST collect the following metrics: IPC, cache miss rate, average memory latency, workload response time
- **EXP-005**: Experiment scripts MUST be reproducible (same configuration produces same results within measurement tolerance)
- **EXP-006**: System MUST support deadline miss detection for real-time workloads (if workload defines deadlines)

#### Repository & Build (REPO-*, BUILD-*)

- **REPO-001**: Repository MUST follow the directory structure defined in the constitution: `src/`, `configs/`, `workloads/`, `scripts/`, `docs/`, `build/`
- **REPO-002**: External dependencies (gem5, Zephyr, NVMain) MUST be managed as Git submodules with pinned versions
- **REPO-003**: Documentation MUST clearly describe directory structure and the role of each directory
- **BUILD-001**: System MUST provide a unified build script (e.g., `scripts/build_all.sh`) to build all components
- **BUILD-002**: All build artifacts MUST be generated under `build/` directory only (source directories remain clean)
- **BUILD-003**: Build scripts MUST support clean builds (remove all build artifacts and rebuild from scratch)
- **BUILD-004**: Documentation MUST provide step-by-step instructions to build and run baseline simulation from clean clone

### Key Entities

- **CPU Configuration**: Represents a specific CPU setup including ISA variant, pipeline parameters, branch predictor type, and frequency
- **Cache Configuration**: Represents L1/L2/L3 cache hierarchy with size, associativity, line size, replacement policy, and write policy for each level
- **Memory Configuration**: Represents memory technology (SRAM/DRAM/STT-MRAM), capacity, latency parameters, and hybrid configurations
- **TCM Configuration**: Represents TCM/TIM setup including size, address range, and code/data section mappings
- **Workload**: Represents a software workload with real-time properties (period, deadline, priority) and expected behavior
- **Simulation Run**: Represents a single gem5 simulation execution with specific CPU/cache/memory/workload configuration and collected metrics
- **Experiment**: Represents a collection of simulation runs comparing different configurations with the same workload

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: From a clean repository clone, a user can build all components and run the baseline simulation successfully within 2 hours (excluding gem5 build time)
- **SC-002**: Baseline simulation boots Zephyr RTOS and completes at least one workload execution without errors
- **SC-003**: System successfully collects and exports at least 5 key metrics (IPC, L1 miss rate, L2 miss rate, average memory latency, execution time) for each simulation run
- **SC-004**: Cache parameter sweep script successfully runs at least 3 different cache configurations and produces comparable results
- **SC-005**: Memory technology comparison successfully runs with DRAM and STT-MRAM configurations and shows measurable latency differences
- **SC-006**: TCM-enabled vs TCM-disabled comparison shows measurable impact on execution time variability (standard deviation or range)
- **SC-007**: All experiment results are reproducible: running the same configuration twice produces metrics within 5% variance
- **SC-008**: Documentation completeness: 100% of configuration parameters are documented with descriptions and valid ranges
- **SC-009**: At least one automotive workload executes with defined periodicity and meets deadlines in baseline configuration
- **SC-010**: Experiment result export includes all configuration parameters and metrics in structured format (CSV/JSON) suitable for automated analysis

## Assumptions

1. **gem5 Compatibility**: Assume gem5 supports RISC-V 32-bit full-system simulation with sufficient maturity for automotive workload evaluation
2. **Zephyr RTOS Support**: Assume Zephyr RTOS has RISC-V 32-bit board support compatible with gem5 simulation environment
3. **NVMain Integration**: Assume NVMain can be integrated with gem5 for STT-MRAM simulation, or alternative memory models are available
4. **Workload Availability**: Assume automotive-representative workloads can be implemented or adapted from existing benchmarks (EEMBC AutoBench kernels or similar)
5. **Simulation Time**: Assume simulation time for typical automotive workloads is reasonable (minutes to hours, not days) for iterative design space exploration
6. **Development Environment**: Assume Ubuntu 24.04 provides all necessary dependencies for gem5, Zephyr, and NVMain builds
7. **Metrics Accuracy**: Assume gem5 statistics provide sufficient accuracy for relative comparisons between configurations (absolute accuracy not required for DSE)
8. **Resource Availability**: Assume development machine has sufficient CPU/memory resources to run gem5 full-system simulations
