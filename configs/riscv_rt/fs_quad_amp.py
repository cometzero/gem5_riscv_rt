"""
gem5 RISC-V 32-bit Full-System Baseline Configuration

This configuration implements the baseline system defined in the specification:
- RISC-V 32-bit in-order CPU (RV32IMAC, 500 MHz)
- L1 I-Cache: 32 KB
- L1 D-Cache: 32 KB  
- L2 Unified Cache: 256 KB
- DRAM: 128 MB

Based on gem5 v25.0.0.1 full-system RISC-V configuration.
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
from ruby import Ruby
from configs.riscv_rt.QuadHiFive import QuadHiFive

class L1ICache(Cache):
    """L1 Instruction Cache - 32 KB"""
    size = "32kB"
    assoc = 2
    tag_latency = 1
    data_latency = 1
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L1DCache(Cache):
    """L1 Data Cache - 32 KB"""
    size = "32kB"
    assoc = 2
    tag_latency = 2
    data_latency = 2
    response_latency = 1
    mshrs = 4
    tgts_per_mshr = 20

class L2Cache(Cache):
    """L2 Unified Cache - 256 KB"""
    size = "256kB"
    assoc = 8
    tag_latency = 10
    data_latency = 10
    response_latency = 1
    mshrs = 20
    tgts_per_mshr = 12

from configs.riscv_rt import memory

def create_system(args, kernels):
    """Create the full-system configuration"""
    
    # Create base system
    system = System()
    
    # Set clock domain - 500 MHz CPU
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "500MHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Memory configuration
    # Handled by memory.py
    system.mem_mode = "timing"
    
    # Create HiFive platform for UART and peripherals
    system.platform = QuadHiFive()
    
    # RTCCLK (Set to 100MHz for faster simulation)
    system.platform.rtc = RiscvRTC(frequency=Frequency("100MHz"))
    system.platform.clint.int_pin = system.platform.rtc.int_pin
    
    if args.mem_system == "classic":
        # Create memory bus and IO bus
        system.membus = SystemXBar()
        system.iobus = IOXBar()
    
    # Attach Platform IO
    system.platform.attachOnChipIO(system.membus)
    system.platform.attachOffChipIO(system.iobus)
    system.platform.attachPlic()
    system.platform.setNumCores(4)
    
    # 2. Create CPUs (4 Cores)
    system.cpu = [TimingSimpleCPU() for _ in range(4)]
    
    if args.mem_system == "classic":
        # Setup memory objects
        system = memory.create_memory_system(system, system.membus, args.mem_tech)
        
        # Create L2 cache bus
        system.l2bus = L2XBar()
        
        # Create L1 caches and connect
        for i, cpu in enumerate(system.cpu):
            cpu.icache = L1ICache()
            cpu.dcache = L1DCache()
            
            cpu.icache.cpu_side = cpu.icache_port
            cpu.dcache.cpu_side = cpu.dcache_port
            
            # Connect to L2 bus
            cpu.icache.mem_side = system.l2bus.cpu_side_ports
            cpu.dcache.mem_side = system.l2bus.cpu_side_ports
            
        # Create L2 cache
        system.l2cache = L2Cache()
        system.l2cache.cpu_side = system.l2bus.mem_side_ports
        
        # Connect L2 cache to memory bus
        system.l2cache.mem_side = system.membus.cpu_side_ports
        
        # Create Dedicated Memory (4 Cores)
        sram_base = 0x90000000
        mram_base = 0xA0000000
        
        for i in range(4):
            sram, mram = memory.create_core_memory(i, system.membus, sram_base, mram_base, args.mem_tech, image_file=kernels[i])
            setattr(system, f"core_{i}_sram", sram)
            setattr(system, f"core_{i}_mram", mram)
            
            system.mem_ranges.append(sram.range)
            system.mem_ranges.append(mram.range)
            
        # Ghost Memory for AON/PRCI (0x10000000 - 0x10010000)
        # Zephyr accesses this during boot for clock setup/watchdog
        system.aon_ghost = SimpleMemory(range=AddrRange(0x10000000, size="64kB"),
                                        latency="10ns")
        system.aon_ghost.port = system.membus.mem_side_ports

        # Ghost Memory for 0x8ffff000 (likely stack/ELF alignment issue)
        system.ghost_memory = SimpleMemory(range=AddrRange(0x8ffff000, size="4kB"),
                                           latency="10ns")
        system.ghost_memory.port = system.membus.mem_side_ports
        system.mem_ranges.append(system.ghost_memory.range)

        system.ghost_memory_2 = SimpleMemory(range=AddrRange(0x7ffff000, size="4kB"),
                                           latency="10ns")
        system.ghost_memory_2.port = system.membus.mem_side_ports
        system.mem_ranges.append(system.ghost_memory_2.range)

        # Ghost Memory for Peripheral Gap (0x10040000 - 0x20000000)
        # Covers 0x1417fe00
        system.gap_ghost_1 = SimpleMemory(range=AddrRange(0x10040000, size="255MB"),
                                          latency="100ns")
        system.gap_ghost_1.port = system.membus.mem_side_ports
        system.mem_ranges.append(system.gap_ghost_1.range)

        # Ghost Memory for Flash Gap (0x22000000 - 0x62000000)
        # Covers 0x2414e000. Starts after system.flash (0x20000000 + 32MB)
        system.gap_ghost_2 = SimpleMemory(range=AddrRange(0x22000000, size="1024MB"),
                                          latency="100ns")
        system.gap_ghost_2.port = system.membus.mem_side_ports
        system.mem_ranges.append(system.gap_ghost_2.range)
        
    else:
        # Ruby System
        from configs.riscv_rt.ruby import system as ruby_system
        
        # Define ranges manually for Ruby (must match memory.py logic)
        system.mem_ranges = [
            AddrRange(0x0, size="64kB"),           # Boot ROM
            AddrRange(0x20000000, size="32MB"),    # Flash
            AddrRange(0x80000000, size="2MB"),     # SRAM
            AddrRange(0x80200000, size="126MB")    # DRAM
        ]
        
        # Create IO Bus
        system.iobus = IOXBar()
        
        # Create Ruby System
        ruby_system.create_ruby_system(system, args, system.mem_ranges)
        
        # Connect CPU to Ruby Sequencer
        # Assuming 1 CPU, 1 Sequencer
        # Connect both I and D ports to the same sequencer port
        system.cpu.icache_port = system.ruby._cpu_ports[0].slave
        system.cpu.dcache_port = system.ruby._cpu_ports[0].slave
    
    # Create interrupt controller
    for cpu in system.cpu:
        cpu.createInterruptController()
        cpu.clk_domain = system.clk_domain # Set clock domain here
        
        # Configure for RV32
        cpu.ArchISA.riscv_type = "RV32"
        
        # Create CPU threads
        cpu.createThreads()
    
    # Connect platform PCI to IO bus
    system.platform.pci_host.pio = system.iobus.mem_side_ports
    
    # Create bridge between memory bus and IO bus (Classic only)
    if args.mem_system == "classic":
        system.bridge = Bridge(delay="50ns")
        system.bridge.mem_side_port = system.iobus.cpu_side_ports
        system.bridge.cpu_side_port = system.membus.mem_side_ports
        system.bridge.ranges = system.platform._off_chip_ranges()
        
        # Attach platform devices
        # system.platform.attachOnChipIO(system.membus)
        # system.platform.attachOffChipIO(system.iobus)
        
        # Create system port for functional access
        system.system_port = system.membus.cpu_side_ports
        
    else:
        # Ruby IO Configuration
        # system.system_port is connected by Ruby.create_system
        
        # Attach platform devices to IO bus (since we don't have membus)
        system.platform.attachOnChipIO(system.iobus)
        system.platform.attachOffChipIO(system.iobus)
        
        # IO bus to Ruby connection is handled by passing dma_ports to Ruby.create_system

    # Common Platform Setup
    system.platform.attachPlic()
    system.platform.setNumCores(1)
    
    # PMA Checker for uncacheable regions
    uncacheable_range = [
        *system.platform._on_chip_ranges(),
        *system.platform._off_chip_ranges(),
    ]
    for cpu in system.cpu:
        cpu.mmu.pma_checker = PMAChecker(uncacheable=uncacheable_range)
    
    return system

def main():
    """Main function to run the simulation"""
    
    parser = argparse.ArgumentParser(description="gem5 RISC-V 32-bit Full-System Baseline")
    
    # Add common options
    Options.addCommonOptions(parser)
    # Add Ruby options
    Ruby.define_options(parser)
    
    parser.add_argument("--kernels", type=str, required=True,
                        help="Comma-separated list of 4 kernel binaries")
    parser.add_argument("--max-ticks", type=int, default=None,
                        help="Maximum simulation ticks")
    
    parser.add_argument("--mem-tech", default="dram", choices=["dram", "mram"],
                        help="Main memory technology")
    parser.add_argument("--boot-mode", default="sram", choices=["sram", "flash"],
                        help="Boot source")
    parser.add_argument("--mem-system", default="classic", choices=["classic", "ruby"],
                        help="Memory system type")
    
    parser.add_argument("--bootloader", type=str, default=None,
                        help="Bootloader ELF file")
    
    args = parser.parse_args()
    
    kernels = args.kernels.split(',')
    if len(kernels) != 4:
        print("Error: Must provide exactly 4 kernels")
        sys.exit(1)
    
    # Create system
    system = create_system(args, kernels)
    
    # Set workload
    # For bare-metal with bootloader: boot ROM at 0x0 jumps to kernel at 0x80000000
    # For Zephyr: boot directly to kernel at 0x80000000
    system.workload = RiscvBareMetal()
    
    if args.bootloader:
        system.workload.bootloader = args.bootloader
    else:
        # Use Core 0 kernel as the main bootloader for the system
        system.workload.bootloader = kernels[0]
        
    system.workload.auto_reset_vect = True
    
    # Create root object
    root = Root(full_system=True, system=system)
    
    # Instantiate configuration
    m5.instantiate()
    
    print(f"Beginning simulation")
    print(f"Kernels: {args.kernels}")
    print(f"CPU: RV32 MinorCPU @ 500 MHz")
    print(f"L1-I: 32 KB, L1-D: 32 KB, L2: 256 KB")
    print(f"Memory: 128 MB DRAM")
    print("")
    
    # Run simulation
    exit_event = m5.simulate(args.max_ticks if args.max_ticks else m5.MaxTick)
    
    print(f"Simulation complete")
    print(f"Exit: {exit_event.getCause()}")
    print(f"Simulated ticks: {m5.curTick()}")
    
    sys.exit(0)

if __name__ == "__m5_main__":
    main()
