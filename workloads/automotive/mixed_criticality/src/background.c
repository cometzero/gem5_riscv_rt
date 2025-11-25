/*
 * Copyright (c) 2024 gem5
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

void background_task(void)
{
    int count = 0;
    while (1) {
        /* Simulate background processing */
        /* This code should reside in DRAM (0x80200000) */
        printk("Background Task: %d (DRAM)\n", count++);
        k_msleep(500); /* 2Hz */
    }
}
