# Makefile for RISC-V 32-bit bare-metal programs
# Requires riscv32-unknown-elf-gcc toolchain

# Toolchain
PREFIX = riscv64-unknown-elf-
CC = $(PREFIX)gcc
LD = $(PREFIX)ld
OBJCOPY = $(PREFIX)objcopy
OBJDUMP = $(PREFIX)objdump

# Compiler flags
CFLAGS = -march=rv32imac -mabi=ilp32 -O2 -nostdlib -nostartfiles -ffreestanding
LDFLAGS = -Tlinker.ld -nostdlib -Wl,-melf32lriscv

# Targets
TARGET = hello
OBJS = $(TARGET).o

all: $(TARGET).elf $(TARGET).bin $(TARGET).dump

$(TARGET).elf: $(OBJS) linker.ld
	$(CC) -march=rv32imac -mabi=ilp32 $(LDFLAGS) -o $@ $(OBJS)

$(TARGET).o: $(TARGET).c
	$(CC) $(CFLAGS) -c -o $@ $<

$(TARGET).bin: $(TARGET).elf
	$(OBJCOPY) -O binary $< $@

$(TARGET).dump: $(TARGET).elf
	$(OBJDUMP) -d $< > $@

clean:
	rm -f *.o *.elf *.bin *.dump

.PHONY: all clean
