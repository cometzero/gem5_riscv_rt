/* Boot ROM for RISC-V gem5 simulation
 * This minimal boot code jumps from reset vector (0x0) to DRAM (0x80000000)
 */

.section .text.boot
.globl _boot
_boot:
    /* Load DRAM base address into t0 */
    lui t0, 0x80000
    
    /* Jump to DRAM where the actual program is loaded */
    jr t0
    
    /* Infinite loop in case we return (should never happen) */
1:
    j 1b
