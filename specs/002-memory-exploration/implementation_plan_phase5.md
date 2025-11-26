# Phase 5 Implementation Plan: STT-MRAM Support

## Goal Description
Implement STT-MRAM (Spin-Transfer Torque Magnetic RAM) modeling support in the gem5 RISC-V simulation framework. This involves adding a new memory type with asymmetric read/write latencies to the `memory.py` configuration and ensuring it can be selected via CLI arguments for both Classic and Ruby memory systems.

## User Review Required
> [!NOTE]
> STT-MRAM latencies are approximated based on typical research values (Read: 20ns, Write: 100ns) as specific device datasheets were not provided.

## Proposed Changes

### Configs

#### [MODIFY] [memory.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/memory.py)
- Import `NVMInterface` from `m5.objects`.
- Define `class STTMRAM(NVMInterface)` with custom parameters:
  - `tREAD`: 20ns
  - `tWRITE`: 100ns
  - `device_size`: 128MB (to match DRAM size for drop-in replacement)
- Update `create_memory_system` to instantiate `STTMRAM` when `mem_type="mram"`.

#### [MODIFY] [base_fs.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/base_fs.py)
- Ensure `--mem-tech` argument is correctly passed to `create_memory_system`.
- (Already implemented, just verification needed).

#### [MODIFY] [system.py](file:///home/ubuntu/work/gem5/gem5_riscv_rt/configs/riscv_rt/ruby/system.py)
- Update `create_ruby_system` to accept `mem_type` argument.
- Configure the Directory Controller for the main memory range to use `STTMRAM` timings if `mem_type="mram"`.

## Verification Plan

### Automated Tests
- Run simulation with `--mem-tech=mram` and `--mem-system=classic`.
  ```bash
  ./scripts/run_sim.sh mram_test src/zephyr/build/zephyr/zephyr.elf 10000000 --boot-mode=sram --mem-tech=mram
  ```
- Check `stats.txt` for `system.mem_ctrl.dram.readBursts` and `writeBursts` and associated latencies (if tracked).
- Verify that simulation completes successfully.

### Manual Verification
- Inspect `config.ini` in the output directory to confirm `type=STTMRAM` (or `NVMInterface`) for the memory controller.
