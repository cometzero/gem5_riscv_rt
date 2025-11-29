"""
QuadHiFive Platform Configuration

Extends the standard HiFive platform to support 4 UARTs for Quad Core AMP.
"""

from m5.objects import *
from m5.util import addToPath

class QuadHiFive(HiFive):
    """
    HiFive Platform with 4 UARTs.
    
    The base HiFive has one UART at 0x10010000 (ID 10).
    We add 3 more at:
    - UART 1: 0x10011000 (ID 10 - Shared)
    - UART 2: 0x10012000 (ID 10 - Shared)
    - UART 3: 0x10013000 (ID 10 - Shared)
    """
    
    # Move PCI Host to avoid conflict with MRAM (0x30000000) and SRAM (0x40000000)
    pci_host = GenericRiscvPciHost(
        conf_base=0x50000000,
        conf_size="256MiB",
        conf_device_bits=12,
        pci_pio_base=0x2F000000,
        pci_mem_base=0x60000000,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Explicitly link base UART to base Terminal to avoid Parent.any ambiguity
        self.uart.device = self.terminal
        # Move UART0 to standard FE310 address (0x10010000) to avoid conflict with PRCI (0x10000000)
        self.uart.pio_addr = 0x10010000
        self.uart.pio_size = 0x100
        
        # UART 1
        self.terminal1 = Terminal()
        self.uart1 = RiscvUart8250(pio_addr=0x10011000, pio_size=0x100, device=self.terminal1, interrupt_id=11)
        
        # UART 2
        self.terminal2 = Terminal()
        self.uart2 = RiscvUart8250(pio_addr=0x10012000, pio_size=0x100, device=self.terminal2, interrupt_id=12)
        
        # UART 3
        self.terminal3 = Terminal()
        self.uart3 = RiscvUart8250(pio_addr=0x10013000, pio_size=0x100, device=self.terminal3, interrupt_id=13)

    # attachOnChipIO is not needed as we rely on _off_chip_devices for UARTs
    # and the base class handles CLINT/PLIC in _on_chip_devices.

    def _on_chip_ranges(self):
        """Return list of on-chip IO ranges"""
        ranges = super()._on_chip_ranges()
        
        # Add ranges for new UARTs (4KB each)
        ranges.append(AddrRange(0x10011000, size="4kB"))
        ranges.append(AddrRange(0x10012000, size="4kB"))
        ranges.append(AddrRange(0x10013000, size="4kB"))
        
        return ranges

    def _off_chip_devices(self):
        """Returns a list of off-chip peripherals"""
        devices = super()._off_chip_devices()
        devices.extend([self.uart1, self.uart2, self.uart3])
        return devices
