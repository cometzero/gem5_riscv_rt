/*
 * Copyright (c) 2024 gem5
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

void critical_task(void)
{
    int count = 0;
    while (1) {
        /* Simulate critical processing */
        /* This code should reside in SRAM (0x80000000) */
        printk("Critical Task: %d (SRAM)\n", count++);
        k_msleep(100); /* 10Hz */
    }
}
