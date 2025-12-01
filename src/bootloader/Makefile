CROSS_COMPILE ?= /home/ubuntu/zephyr-sdk-0.16.8/riscv64-zephyr-elf/bin/riscv64-zephyr-elf-
CC = $(CROSS_COMPILE)gcc
OBJCOPY = $(CROSS_COMPILE)objcopy

CFLAGS = -march=rv32imac_zicsr -mabi=ilp32 -nostdlib -n -Ttext 0x80000000

all: bootloader.elf

bootloader.elf: boot.S
	$(CC) $(CFLAGS) $< -o $@

clean:
	rm -f bootloader.elf
