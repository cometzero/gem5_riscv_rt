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

def create_system(args):
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
    
    # Memory configuration
    system.mem_mode = "timing"

    # Create RISC-V 32-bit CPU
    # Use TimingSimpleCPU for Ruby compatibility/debugging
    system.cpu = TimingSimpleCPU()
    system.cpu.clk_domain = system.clk_domain
    
    if args.mem_system == "classic":
        # Create memory bus and IO bus
        system.membus = SystemXBar()
        system.iobus = IOXBar()
        
        # Setup memory objects
        system = memory.create_memory_system(system, system.membus, args.mem_tech)
        
        # Create L1 caches
        system.cpu.icache = L1ICache()
        system.cpu.dcache = L1DCache()
        
        # Connect L1 caches to CPU
        system.cpu.icache.cpu_side = system.cpu.icache_port
        system.cpu.dcache.cpu_side = system.cpu.dcache_port
        
        # Create L2 cache bus
        system.l2bus = L2XBar()
        
        # Connect L1 caches to L2 bus
        system.cpu.icache.mem_side = system.l2bus.cpu_side_ports
        system.cpu.dcache.mem_side = system.l2bus.cpu_side_ports
        
        # Create L2 cache
        system.l2cache = L2Cache()
        system.l2cache.cpu_side = system.l2bus.mem_side_ports
        
        # Connect L2 cache to memory bus
        system.l2cache.mem_side = system.membus.cpu_side_ports
        
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
    system.cpu.createInterruptController()
    
    # Configure for RV32
    system.cpu.ArchISA.riscv_type = "RV32"
    
    # Create CPU threads
    system.cpu.createThreads()
    
    # Create HiFive platform for UART and peripherals
    system.platform = HiFive()
    
    # RTCCLK (Set to 100MHz for faster simulation)
    system.platform.rtc = RiscvRTC(frequency=Frequency("100MHz"))
    system.platform.clint.int_pin = system.platform.rtc.int_pin
    
    # Connect platform PCI to IO bus
    system.platform.pci_host.pio = system.iobus.mem_side_ports
    
    # Create bridge between memory bus and IO bus (Classic only)
    if args.mem_system == "classic":
        system.bridge = Bridge(delay="50ns")
        system.bridge.mem_side_port = system.iobus.cpu_side_ports
        system.bridge.cpu_side_port = system.membus.mem_side_ports
        system.bridge.ranges = system.platform._off_chip_ranges()
        
        # Attach platform devices
        system.platform.attachOnChipIO(system.membus)
        system.platform.attachOffChipIO(system.iobus)
        
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
    system.cpu.mmu.pma_checker = PMAChecker(uncacheable=uncacheable_range)
    
    return system

def main():
    """Main function to run the simulation"""
    
    parser = argparse.ArgumentParser(description="gem5 RISC-V 32-bit Full-System Baseline")
    
    # Add common options
    Options.addCommonOptions(parser)
    # Add Ruby options
    Ruby.define_options(parser)
    
    parser.add_argument("--kernel", type=str, required=True,
                        help="Path to kernel/bare-metal binary (ELF)")
    parser.add_argument("--max-ticks", type=int, default=None,
                        help="Maximum simulation ticks")
    
    parser.add_argument("--mem-tech", default="dram", choices=["dram", "mram"],
                        help="Main memory technology")
    parser.add_argument("--boot-mode", default="sram", choices=["sram", "flash"],
                        help="Boot source")
    parser.add_argument("--mem-system", default="classic", choices=["classic", "ruby"],
                        help="Memory system type")
    
    args = parser.parse_args()
    
    # Create system
    system = create_system(args)
    
    # Set workload
    # For bare-metal with bootloader: boot ROM at 0x0 jumps to kernel at 0x80000000
    # For Zephyr: boot directly to kernel at 0x80000000
    system.workload = RiscvBareMetal()
    
    bootloader_path = Path(args.kernel).parent / "boot.elf"
    if bootloader_path.exists():
        # Bare-metal mode with bootloader
        system.workload.bootloader = str(bootloader_path)
        system.workload.auto_reset_vect = False
        system.workload.reset_vect = 0x0  # Start at boot ROM
    else:
        # Zephyr mode - boot directly to kernel
        system.workload.bootloader = args.kernel
        system.workload.auto_reset_vect = True  # Use entry point from ELF
    
    # Create root object
    root = Root(full_system=True, system=system)
    
    # Instantiate configuration
    m5.instantiate()
    
    print(f"Beginning simulation")
    print(f"Kernel: {args.kernel}")
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
