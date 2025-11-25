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

from common import Options
from common import Simulation
from common.Caches import *

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

def create_system():
    """Create the full-system configuration"""
    
    # Create base system
    system = System()
    
    # Set clock domain - 500 MHz CPU
    system.clk_domain = SrcClockDomain()
    system.clk_domain.clock = "500MHz"
    system.clk_domain.voltage_domain = VoltageDomain()
    
    # Memory configuration
    # Boot ROM at 0x0 (64 KB) - contains bootloader
    # DRAM at 0x80000000 (128 MB) - contains main program
    system.mem_mode = "timing"
    system.mem_ranges = [
        AddrRange(start=0x0, size="64kB"),           # Boot ROM
        AddrRange(start=0x80000000, size="128MB")     # DRAM
    ]
    
    # Create RISC-V 32-bit in-order CPU
    system.cpu = MinorCPU()
    system.cpu.clk_domain = system.clk_domain
    
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
    
    # Create memory bus and IO bus
    system.membus = SystemXBar()
    system.iobus = IOXBar()
    
    # Connect L2 cache to memory bus
    system.l2cache.mem_side = system.membus.cpu_side_ports
    
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
    
    # Create bridge between memory bus and IO bus
    system.bridge = Bridge(delay="50ns")
    system.bridge.mem_side_port = system.iobus.cpu_side_ports
    system.bridge.cpu_side_port = system.membus.mem_side_ports
    system.bridge.ranges = system.platform._off_chip_ranges()
    
    # Attach platform devices
    system.platform.attachOnChipIO(system.membus)
    system.platform.attachOffChipIO(system.iobus)
    system.platform.attachPlic()
    system.platform.setNumCores(1)
    
    # PMA Checker for uncacheable regions
    uncacheable_range = [
        *system.platform._on_chip_ranges(),
        *system.platform._off_chip_ranges(),
    ]
    system.cpu.mmu.pma_checker = PMAChecker(uncacheable=uncacheable_range)
    
    # Create boot ROM controller (read-only memory at 0x0)
    system.boot_rom = SimpleMemory()
    system.boot_rom.range = system.mem_ranges[0]  # 0x0 - 0x10000
    system.boot_rom.port = system.membus.mem_side_ports
    
    # Create DRAM controller  
    system.mem_ctrl = MemCtrl()
    system.mem_ctrl.dram = DDR3_1600_8x8()
    system.mem_ctrl.dram.range = system.mem_ranges[1]  # 0x80000000 - 0x88000000
    system.mem_ctrl.port = system.membus.mem_side_ports
    
    # Create system port for functional access
    system.system_port = system.membus.cpu_side_ports
    
    return system

def main():
    """Main function to run the simulation"""
    
    parser = argparse.ArgumentParser(description="gem5 RISC-V 32-bit Full-System Baseline")
    parser.add_argument("--kernel", type=str, required=True,
                        help="Path to kernel/bare-metal binary (ELF)")
    parser.add_argument("--max-ticks", type=int, default=None,
                        help="Maximum simulation ticks")
    
    args = parser.parse_args()
    
    # Create system
    system = create_system()
    
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
