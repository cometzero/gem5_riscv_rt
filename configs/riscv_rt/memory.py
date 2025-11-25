"""
Memory Configuration for RISC-V Real-Time System

Defines the heterogeneous memory map including:
- Boot ROM: 0x0 (64KB)
- NOR Flash: 0x20000000 (32MB)
- SRAM: 0x80000000 (2MB)
- Main Memory (DRAM/MRAM): 0x80200000 (126MB)
"""

from m5.objects import *

def create_memory_system(system, membus, mem_type="dram"):
    """
    Create the memory objects and attach them to the memory bus.
    
    Args:
        system: The gem5 System object
        membus: The system memory bus (SystemXBar)
        mem_type: "dram" or "mram"
    """
    
    # 1. Boot ROM (0x0 - 0x10000)
    # Contains bootloader or reset vector jump
    system.boot_rom = SimpleMemory(range=AddrRange(0x0, size="64kB"),
                                   latency="10ns")
    system.boot_rom.port = membus.mem_side_ports
    
    # 2. NOR Flash (0x20000000 - 0x22000000)
    # Used for XIP boot or storage
    system.flash = SimpleMemory(range=AddrRange(0x20000000, size="32MB"),
                                latency="100ns",
                                bandwidth="100MB/s")
    system.flash.port = membus.mem_side_ports
    
    # 3. SRAM (0x80000000 - 0x80200000)
    # Fast on-chip memory for critical code/data
    system.sram = SimpleMemory(range=AddrRange(0x80000000, size="2MB"),
                               latency="1ns",
                               bandwidth="10GB/s")
    system.sram.port = membus.mem_side_ports
    
    # 4. Main Memory (0x80200000 - 0x88000000)
    # DRAM or STT-MRAM
    dram_range = AddrRange(0x80200000, size="126MB")
    
    system.mem_ctrl = MemCtrl()
    
    if mem_type == "dram":
        # Standard DDR3
        system.mem_ctrl.dram = DDR3_1600_8x8()
    elif mem_type == "mram":
        # STT-MRAM Model (Placeholder using modified DDR3 for now)
        # Will be replaced by NVMInterface in Phase 5
        system.mem_ctrl.dram = DDR3_1600_8x8()
        system.mem_ctrl.dram.tCL = "10ns"   # Fast Read
        system.mem_ctrl.dram.tCWL = "50ns"  # Slow Write
        
    system.mem_ctrl.dram.range = dram_range
    system.mem_ctrl.port = membus.mem_side_ports
    
    # Set system memory ranges for Ruby/System checks
    system.mem_ranges = [
        system.boot_rom.range,
        system.flash.range,
        system.sram.range,
        dram_range
    ]
    
    return system
