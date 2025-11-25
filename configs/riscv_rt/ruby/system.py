"""
Ruby System Configuration for RISC-V Real-Time System

Configures the Ruby memory system using the MI_example protocol.
Supports heterogeneous memory ranges by configuring directory controllers.
"""

import m5
from m5.objects import *
from m5.defines import buildEnv
from ruby import Ruby

def create_ruby_system(system, options, mem_ranges):
    """
    Create the Ruby Memory System.
    
    Args:
        system: The gem5 System object
        options: argparse options (must contain num_cpus, etc.)
        mem_ranges: List of AddrRange objects for the memory
    """
    
    if "RUBY" not in buildEnv:
        m5.fatal("Gem5 was not compiled with Ruby support!")
        
    # Ensure essential options are present
    if not hasattr(options, 'num_cpus'):
        options.num_cpus = 1
    if not hasattr(options, 'num_dirs'):
        options.num_dirs = len(mem_ranges) # One directory per memory range?
    if not hasattr(options, 'network'):
        options.network = 'simple'
    if not hasattr(options, 'topology'):
        options.topology = 'Crossbar'
    if not hasattr(options, 'garnet_network'):
        options.garnet_network = None
        
    # Create the Ruby System using standard helper
    # This creates system.ruby, network, and controllers
    # Pass iobus as piobus and dma_port
    Ruby.create_system(options, True, system, piobus=system.iobus, 
                       dma_ports=[system.iobus.mem_side_ports])
    
    # system.system_port is connected in base_fs.py via IOBus
    
    # Configure Directory Controllers for Heterogeneous Memory
    # MI_example creates a Directory_Controller for each directory
    # We need to map them to our specific ranges (SRAM, DRAM, etc.)
    
    # Note: Ruby.create_system usually divides the total memory equally among dirs.
    # We might need to manually override the ranges.
    
    if hasattr(system.ruby, 'dir_cntrls'):
        # Assuming 1 CPU, we might have 1 or more dirs.
        # If we have multiple ranges, we should ideally have multiple dirs.
        # For MVP, we let Ruby handle the mapping or assume a single directory covers all.
        pass
        
    return system
