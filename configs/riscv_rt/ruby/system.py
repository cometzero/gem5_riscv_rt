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
    print("DEBUG: Entering create_ruby_system")
    
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
    
    print(f"DEBUG: system.ruby type: {type(system.ruby)}")
    # print(f"DEBUG: system.ruby attrs: {dir(system.ruby)}")
    
    if hasattr(system, 'mem_ctrls'):
        # Import STTMRAM if needed
        from configs.riscv_rt.memory import STTMRAM
        
        print(f"DEBUG: system.mem_ctrls len: {len(system.mem_ctrls)}")
        for i, mc in enumerate(system.mem_ctrls):
            # Determine range
            r = None
            if isinstance(mc, m5.objects.MemCtrl):
                r = mc.dram.range
            elif hasattr(mc, 'range'):
                r = mc.range
            
            print(f"DEBUG: MemCtrl {i}: {type(mc)} range={r} start={r.start if r else 'N/A'}")
            
            # Check if this is Main Memory (0x80200000)
            if r and int(r.start) == 0x80200000:
                print(f"DEBUG: options.mem_tech={getattr(options, 'mem_tech', 'N/A')}")
                if getattr(options, 'mem_tech', 'dram') == 'mram':
                    print(f"Info: Replacing Memory Controller {i} with STT-MRAM")
                    
                    # Create new STTMRAM controller
                    new_intf = STTMRAM()
                    new_intf.range = r
                    
                    new_ctrl = m5.objects.MemCtrl()
                    new_ctrl.dram = new_intf
                    new_ctrl.clk_domain = system.clk_domain
                    
                    # Connect to crossbar
                    # Assuming 1 directory or mapping logic holds
                    num_ranges = len(mem_ranges)
                    dir_index = i // num_ranges
                    
                    if hasattr(system.ruby, 'crossbars'):
                        xbar = system.ruby.crossbars[dir_index]
                        new_ctrl.port = xbar.mem_side_ports
                        
                        # Parent the new controller explicitly
                        system.mram_ctrl = new_ctrl
                        
                        # Disable the old controller by setting range to a safe unused address
                        # We do NOT update system.mem_ctrls to avoid SimObjectVector parenting issues
                        old_ctrl = system.mem_ctrls[i]
                        
                        # Check if old_ctrl is MemCtrl or SimpleMemory
                        from m5.objects import AddrRange
                        # Use a high address that is unlikely to be accessed
                        safe_range = AddrRange(0x90000000, size=64)
                        
                        if hasattr(old_ctrl, 'dram'):
                            old_ctrl.dram.range = safe_range
                        else:
                            old_ctrl.range = safe_range
                        
                        # Also ensure clk_domain is set on new controller
                        new_ctrl.clk_domain = system.clk_domain
                        new_intf.clk_domain = system.clk_domain
                        
                        print(f"DEBUG: Disabled old controller {i} by moving to {safe_range}")
                        print(f"DEBUG: system.clk_domain={system.clk_domain}")
                        print(f"DEBUG: new_ctrl.clk_domain={new_ctrl.clk_domain}")
                    else:
                        print("Warning: Could not find crossbar to connect STT-MRAM. Skipping replacement.")

    return system
