"""
gem5 RISC-V Octa-Core Hybrid AMP/SMP Configuration

Architecture:
- 8x RISC-V RV32IMAC Cores @ 500 MHz
- Cluster 0 (Cores 0-3): AMP Mode
    - Independent Zephyr kernels
    - Dedicated SRAM (1MB) / MRAM (2MB) per core
    - Shared L2 Cache (Cluster 0)
    - Dedicated UARTs (UART0-3)
- Cluster 1 (Cores 4-7): SMP Mode
    - Single Zephyr SMP kernel
    - Shared SRAM (4MB) / MRAM (8MB)
    - Shared L2 Cache (Cluster 1)
    - Shared UART (UART4)

Memory Map:
- Boot ROM: 0x0
- Flash: 0x20000000
- Cluster 0 SRAM: 0x90000000 (4x 1MB)
- Cluster 0 MRAM: 0xA0000000 (4x 2MB)
- Cluster 1 SRAM: 0x90400000 (4MB)
- Cluster 1 MRAM: 0x80000000 (8MB) - Note: Mapped to standard Zephyr load address
"""

import argparse
import sys
from pathlib import Path

import m5
from m5.objects import *
from m5.util import addToPath

# Add gem5 configs to path
addToPath("../../src/gem5/configs")
# Add project root to path for local configs
addToPath("../../")

from common import Options
from common import Simulation
from common.Caches import *
from configs.riscv_rt.OctaHiFive import OctaHiFive
from configs.riscv_rt import memory

class L1ICache(Cache):
    size = "32kB"
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L1DCache(Cache):
    size = "32kB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L2Cache(Cache):
    size = "256kB"
    assoc = 8
    tag_latency = 10
    data_latency = 10
    response_latency = 1
    mshrs = 20
    tgts_per_mshr = 12

def create_system(args, kernels):
    # Create base system
    system = System()
    
    # Set clock domain - 500 MHz CPU
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "500MHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    
    system.mem_mode = "timing"
    
    # Create OctaHiFive platform
    system.platform = OctaHiFive()
    
    # RTCCLK
    system.platform.rtc = RiscvRTC(frequency=Frequency("100MHz"))
    system.platform.clint.int_pin = system.platform.rtc.int_pin
    
    # Create memory bus and IO bus
    system.membus = SystemXBar()
    system.iobus = IOXBar()
    
    # Attach Platform IO
    system.platform.attachOnChipIO(system.membus)
    system.platform.attachOffChipIO(system.iobus)
    system.platform.attachPlic()
    system.platform.setNumCores(8)
    
    # Create CPUs
    system.cpu = [RiscvO3CPU(cpu_id=i) for i in range(8)]
    
    # Create CPUs
    system.cpu = [RiscvO3CPU(cpu_id=i) for i in range(8)]
    
    # ISA configuration removed (relying on default RV64)
    
    # Create L2 Buses (One per cluster)
    system.l2bus0 = L2XBar() # Cluster 0
    system.l2bus1 = L2XBar() # Cluster 1
    
    # Create L1 caches and connect
    for i, cpu in enumerate(system.cpu):
        cpu.icache = L1ICache()
        cpu.dcache = L1DCache()
        
        cpu.icache.cpu_side = cpu.icache_port
        cpu.dcache.cpu_side = cpu.dcache_port
        
        # Connect to appropriate L2 bus
        if i < 4: # Cluster 0 (Cores 0-3)
            cpu.icache.mem_side = system.l2bus0.cpu_side_ports
            cpu.dcache.mem_side = system.l2bus0.cpu_side_ports
        else: # Cluster 1 (Cores 4-7)
            cpu.icache.mem_side = system.l2bus1.cpu_side_ports
            cpu.dcache.mem_side = system.l2bus1.cpu_side_ports
            
    # Create L2 Caches (One per cluster)
    system.l2cache0 = L2Cache()
    system.l2cache0.cpu_side = system.l2bus0.mem_side_ports
    system.l2cache0.mem_side = system.membus.cpu_side_ports
    
    system.l2cache1 = L2Cache()
    system.l2cache1.cpu_side = system.l2bus1.mem_side_ports
    system.l2cache1.mem_side = system.membus.cpu_side_ports
    
    # Memory Setup
    system = memory.create_memory_system(system, system.membus, args.mem_tech, create_default_ram=False)
    
    # Cluster 0 Memory (Dedicated)
    sram_base_c0 = 0x90000000
    mram_base_c0 = 0xA0000000
    
    for i in range(4):
        sram, mram = memory.create_core_memory(i, system.membus, sram_base_c0, mram_base_c0, args.mem_tech, image_file=kernels[i])
        setattr(system, f"core_{i}_sram", sram)
        setattr(system, f"core_{i}_mram", mram)
        system.mem_ranges.append(sram.range)
        system.mem_ranges.append(mram.range)
        
    # Cluster 1 Memory (Shared)
    # MRAM at 0x80000000 (Standard Zephyr Load Address)
    # SRAM at 0x90400000 (After Cluster 0 SRAMs)
    sram_base_c1 = 0x90400000
    mram_base_c1 = 0x80000000
    
    # Use the 5th kernel argument for the SMP image
    smp_kernel = kernels[4] if len(kernels) > 4 else None
    
    sram_c1, mram_c1 = memory.create_cluster_memory(1, system.membus, sram_base_c1, mram_base_c1, sram_size="4MB", mram_size="8MB", image_file=smp_kernel)
    system.c1_sram = sram_c1
    system.c1_mram = mram_c1
    system.mem_ranges.append(sram_c1.range)
    system.mem_ranges.append(mram_c1.range)

    # Ghost Memories (Copy from QuadHiFive config)
    system.aon_ghost = SimpleMemory(range=AddrRange(0x10000000, size="64kB"), latency="10ns")
    system.aon_ghost.port = system.membus.mem_side_ports
    
    system.gap_ghost_1 = SimpleMemory(range=AddrRange(0x10040000, size="255MB"), latency="100ns")
    system.gap_ghost_1.port = system.membus.mem_side_ports
    system.mem_ranges.append(system.gap_ghost_1.range)

    # Interrupt Controllers
    for cpu in system.cpu:
        cpu.createInterruptController()
        cpu.clk_domain = system.clk_domain
        cpu.ArchISA.riscv_type = "RV32"
        cpu.createThreads()
        
    # Connect PCI
    system.platform.pci_host.pio = system.iobus.mem_side_ports
    
    # Bridge
    system.bridge = Bridge(delay="50ns")
    system.bridge.mem_side_port = system.iobus.cpu_side_ports
    system.bridge.cpu_side_port = system.membus.mem_side_ports
    system.bridge.ranges = system.platform._off_chip_ranges()
    
    system.system_port = system.membus.cpu_side_ports
    
    # PMA Checker
    uncacheable_range = [
        *system.platform._on_chip_ranges(),
        *system.platform._off_chip_ranges(),
    ]
    for cpu in system.cpu:
        cpu.mmu.pma_checker = PMAChecker(uncacheable=uncacheable_range)
        
    return system

def main():
    parser = argparse.ArgumentParser(description="gem5 RISC-V Octa-Core Hybrid AMP/SMP")
    Options.addCommonOptions(parser)
    
    parser.add_argument("--kernels", type=str, required=True,
                        help="Comma-separated list of 5 kernel binaries (4 AMP + 1 SMP)")
    parser.add_argument("--max-ticks", type=int, default=None,
                        help="Maximum simulation ticks")
    parser.add_argument("--mem-tech", default="dram", choices=["dram", "mram"],
                        help="Main memory technology")
    parser.add_argument("--bootloader", type=str, default=None,
                        help="Bootloader ELF file")
                        
    args = parser.parse_args()
    
    kernels = args.kernels.split(',')
    if len(kernels) != 5:
        print("Error: Must provide exactly 5 kernels (4 AMP + 1 SMP)")
        sys.exit(1)
        
    system = create_system(args, kernels)
    
    system.workload = RiscvBareMetal()
    if args.bootloader:
        system.workload.bootloader = args.bootloader
    else:
        system.workload.bootloader = kernels[0]
    system.workload.auto_reset_vect = True
    
    root = Root(full_system=True, system=system)
    m5.instantiate()
    
    print(f"Beginning Octa-Core Simulation")
    exit_event = m5.simulate(args.max_ticks if args.max_ticks else m5.MaxTick)
    print(f"Exiting @ tick {m5.curTick()} because {exit_event.getCause()}")

if __name__ == "__m5_main__":
    main()
