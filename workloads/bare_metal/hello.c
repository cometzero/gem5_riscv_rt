/*
 * Simple bare-metal "Hello from RISC-V" program
 * For gem5 RISC-V 32-bit full-system simulation
 * 
 * This program writes a message to UART and exits.
 */

#define UART_BASE 0x10000000

volatile char *uart = (volatile char *)UART_BASE;

void uart_puts(const char *s) {
    while (*s) {
        *uart = *s++;
    }
}

void _start(void) {
    uart_puts("Hello from RISC-V\n");
    uart_puts("gem5 Full-System Simulation\n");
    uart_puts("CPU: RV32IMAC @ 500 MHz\n");
    uart_puts("L1-I: 32 KB, L1-D: 32 KB, L2: 256 KB\n");
    uart_puts("Memory: 128 MB DRAM\n");
    uart_puts("\nBare-metal test complete.\n");
    
    // Exit simulation (gem5 m5 exit)
    // For bare-metal, we just infinite loop
    while (1) {
        __asm__ volatile ("wfi");  // Wait for interrupt
    }
}
