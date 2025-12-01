"""
Memory Configuration for RISC-V Real-Time System

Defines the heterogeneous memory map including:
- Boot ROM: 0x0 (64KB)
- NOR Flash: 0x20000000 (32MB)
- SRAM: 0x80000000 (2MB)
- Main Memory (DRAM/MRAM): 0x80200000 (126MB)
"""

from m5.objects import *

class STTMRAM(NVMInterface):
    """
    STT-MRAM Memory Model
    Based on NVMInterface with asymmetric read/write latencies.
    """
    # 128MB device size to match our DRAM configuration
    device_size = "128MB"
    
    # Timing parameters (approximate for STT-MRAM)
    # Read: Fast, similar to DRAM (~20ns)
    # Write: Slow, significantly higher than DRAM (~100ns)
    tREAD = "20ns"
    tWRITE = "100ns"
    tSEND = "10ns"
    
    # Interface parameters
    device_bus_width = 8
    burst_length = 8
    devices_per_rank = 8
    ranks_per_channel = 1
    banks_per_rank = 8
    
    # Required by MemInterface
    device_rowbuffer_size = "256B"
    
    # Buffer sizes
    write_buffer_size = 64
    read_buffer_size = 32
    
    # Required for stats (must be > 1)
    max_pending_writes = 8
    max_pending_reads = 8
    
    # Timing
    tCK = "1ns"
    tBURST = "4ns"
    tWTR = "2ns"
    tRTW = "2ns"
    tCS = "2ns"
    
    # STT-MRAM Latencies (Asymmetric)
    # Read is faster than Write

def create_memory_system(system, membus, mem_type="dram", create_default_ram=True):
    """
    Create the memory objects and attach them to the memory bus.
    
    Args:
        system: The gem5 System object
        membus: The system memory bus (SystemXBar)
        mem_type: "dram" or "mram"
        create_default_ram: Whether to create default SRAM and Main Memory
    """
    
    # 1. Boot ROM (0x0 - 0x10000)
    # Contains bootloader or reset vector jump
    system.boot_rom = SimpleMemory(range=AddrRange(0x0, size="64kB"),
                                   latency="10ns")
    system.boot_rom.port = membus.mem_side_ports
    
    # 2. NOR Flash (0x20000000 - 0x40000000)
    # Used for XIP boot or storage
    system.flash = SimpleMemory(range=AddrRange(0x20000000, size="512MB"),
                                latency="100ns",
                                bandwidth="100MB/s")
    system.flash.port = membus.mem_side_ports
    
    # Set system memory ranges for Ruby/System checks
    system.mem_ranges = [
        system.boot_rom.range,
        system.flash.range
    ]

    if create_default_ram:
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
            # STT-MRAM Model
            system.mem_ctrl.dram = STTMRAM()
            
        system.mem_ctrl.dram.range = dram_range
        system.mem_ctrl.port = membus.mem_side_ports
        
        system.mem_ranges.append(system.sram.range)
        system.mem_ranges.append(dram_range)
    
    return system

def create_core_memory(core_idx, membus, sram_base, mram_base, mem_type="mram", image_file=None):
    """
    Create dedicated SRAM and MRAM for a specific core.
    
    Args:
        core_idx: Index of the core (0-3)
        membus: The system memory bus
        sram_base: Base address for SRAM
        mram_base: Base address for MRAM
        mem_type: "dram" or "mram" (default mram)
        image_file: Optional path to binary to load into SRAM
        
    Returns:
        Tuple of (sram_obj, mram_ctrl_obj)
    """
    
    # SRAM: 1MB per core
    sram_size = "1MB"
    sram_addr = sram_base + (core_idx * 0x100000) # 1MB offset
    
    sram = SimpleMemory(range=AddrRange(sram_addr, size=sram_size),
                        latency="1ns",
                        bandwidth="10GB/s")
    
    if image_file:
        sram.image_file = image_file
        
    sram.port = membus.mem_side_ports
    
    # MRAM: 2MB per core
    mram_size = "2MB"
    mram_addr = mram_base + (core_idx * 0x200000) # 2MB offset
    
    # Use SimpleMemory for MRAM to avoid MemCtrl crash
    mram = SimpleMemory(range=AddrRange(mram_addr, size=mram_size),
                        latency="30ns", # Approximate MRAM latency
                        bandwidth="100MB/s")
    mram.port = membus.mem_side_ports
    
    return sram, mram

def create_cluster_memory(cluster_id, membus, sram_base, mram_base, sram_size="4MB", mram_size="8MB", image_file=None):
    """
    Create shared SRAM and MRAM for a cluster of cores.
    
    Args:
        cluster_id: ID of the cluster (for naming)
        membus: The system memory bus
        sram_base: Base address for shared SRAM
        mram_base: Base address for shared MRAM
        sram_size: Size of shared SRAM
        mram_size: Size of shared MRAM
        image_file: Optional path to binary to load into shared SRAM
        
    Returns:
        Tuple of (sram_obj, mram_obj)
    """
    
    # Shared SRAM
    sram = SimpleMemory(range=AddrRange(sram_base, size=sram_size),
                        latency="1ns",
                        bandwidth="10GB/s")
    
    if image_file:
        sram.image_file = image_file
        
    sram.port = membus.mem_side_ports
    
    # Shared MRAM
    mram = SimpleMemory(range=AddrRange(mram_base, size=mram_size),
                        latency="30ns",
                        bandwidth="100MB/s")
    
    mram.port = membus.mem_side_ports
    
    return sram, mram
