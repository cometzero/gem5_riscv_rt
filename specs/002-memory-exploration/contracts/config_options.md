# Contract: Simulation Configuration Options

## CLI Arguments (`run_sim.sh` / `configs/riscv_rt/ruby/system.py`)

### Memory Configuration

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--mem-type` | `dram`, `mram`, `hybrid` | `dram` | Main memory technology type. |
| `--sram-size`| `2MB`, `4MB`, ... | `2MB` | Size of the SRAM region. |
| `--boot-mode`| `sram`, `flash` | `sram` | Boot source location. |

### Ruby Protocol

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--ruby-protocol` | `MI_example`, `MESI_Two_Level` | `MI_example` | Coherence protocol to use. |

### Workload Parameters

| Argument | Values | Default | Description |
|----------|--------|---------|-------------|
| `--workload-mix` | `baseline`, `critical-sram` | `baseline` | Workload placement strategy. |
