/*
 * Copyright (c) 2024 gem5
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>

/* Thread Priorities */
#define CRITICAL_PRIORITY -1
#define BACKGROUND_PRIORITY 0

/* Stack Sizes */
#define STACK_SIZE 1024

/* External Functions */
extern void critical_task(void);
extern void background_task(void);

/* Thread Stacks */
K_THREAD_STACK_DEFINE(critical_stack, STACK_SIZE);
K_THREAD_STACK_DEFINE(background_stack, STACK_SIZE);

/* Thread Data */
struct k_thread critical_thread_data;
struct k_thread background_thread_data;

/* Entry Points */
void critical_entry(void *p1, void *p2, void *p3)
{
    critical_task();
}

void background_entry(void *p1, void *p2, void *p3)
{
    background_task();
}

int main(void)
{
    printk("Gem5 RISC-V Mixed Criticality Workload Starting...\n");

    /* Spawn Critical Thread */
    k_thread_create(&critical_thread_data, critical_stack,
                    K_THREAD_STACK_SIZEOF(critical_stack),
                    critical_entry, NULL, NULL, NULL,
                    CRITICAL_PRIORITY, 0, K_NO_WAIT);

    /* Spawn Background Thread */
    k_thread_create(&background_thread_data, background_stack,
                    K_THREAD_STACK_SIZEOF(background_stack),
                    background_entry, NULL, NULL, NULL,
                    BACKGROUND_PRIORITY, 0, K_NO_WAIT);

    return 0;
}
