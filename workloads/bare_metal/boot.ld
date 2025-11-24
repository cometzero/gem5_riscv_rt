/* Linker script for boot ROM */

OUTPUT_ARCH(riscv)
ENTRY(_boot)

SECTIONS
{
    . = 0x0;
    
    .text : {
        *(.text.boot)
        *(.text*)
    }
    
    /* Ensure the boot ROM is small and fits in expected location */
    . = ALIGN(4);
    _end = .;
}
