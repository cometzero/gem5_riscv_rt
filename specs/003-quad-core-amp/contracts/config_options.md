# Configuration Options: Quad Core AMP

**Feature**: Quad Core AMP Zephyr
**Status**: Draft

## CLI Arguments

The `fs_quad_amp.py` script (or modified `base_fs.py`) will accept the following arguments:

### Required

- `--kernel`: Path to the kernel binary for Core 0 (or a list/pattern).
  - *Refinement*: To support 4 distinct kernels, we might need `--kernel0`, `--kernel1`, etc., or a comma-separated list.
  - **Contract**: `--kernels <path0>,<path1>,<path2>,<path3>`

### Optional

- `--mem-tech`: "mram" (Fixed for this feature as per spec, but good to keep configurable if needed).
- `--uart-base`: Base address for UARTs (Default: 0x10010000).
- `--sram-base`: Base address for SRAMs (Default: 0x40000000).
- `--mram-base`: Base address for MRAMs (Default: 0x30000000).

## Output Artifacts

- `m5out/system.pc.com_1.device`: UART output for Core 0
- `m5out/system.pc.com_2.device`: UART output for Core 1
- `m5out/system.pc.com_3.device`: UART output for Core 2
- `m5out/system.pc.com_4.device`: UART output for Core 3
