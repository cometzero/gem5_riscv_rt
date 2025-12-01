"""
OctaHiFive Platform Configuration

Extends the QuadHiFive platform to support 5 UARTs for Octa-Core AMP/SMP.
- Cluster 0 (AMP): UART0-3 (Dedicated)
- Cluster 1 (SMP): UART4 (Shared)
"""

from m5.objects import *
from m5.util import addToPath
from configs.riscv_rt.QuadHiFive import QuadHiFive

class OctaHiFive(QuadHiFive):
    """
    HiFive Platform with 5 UARTs.
    
    Inherits UART0-3 from QuadHiFive.
    Adds UART4 at 0x10014000 (ID 14) for Cluster 1 (SMP).
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # UART 4 (Shared for Cluster 1)
        self.terminal4 = Terminal()
        self.uart4 = RiscvUart8250(pio_addr=0x10014000, pio_size=0x100, device=self.terminal4, interrupt_id=14)

    def _on_chip_ranges(self):
        """Return list of on-chip IO ranges"""
        ranges = super()._on_chip_ranges()
        
        # Add range for UART4 (4KB)
        ranges.append(AddrRange(0x10014000, size="4kB"))
        
        return ranges

    def _off_chip_devices(self):
        """Returns a list of off-chip peripherals"""
        devices = super()._off_chip_devices()
        devices.append(self.uart4)
        return devices
