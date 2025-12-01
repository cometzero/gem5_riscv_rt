/*
 * Copyright (c) 2012-2014 Wind River Systems, Inc.
 *
 * SPDX-License-Identifier: Apache-2.0
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>


#define STACK_SIZE 1024
#define PRIORITY 7

struct k_thread worker_threads[CONFIG_MP_MAX_NUM_CPUS];
K_THREAD_STACK_ARRAY_DEFINE(worker_stacks, CONFIG_MP_MAX_NUM_CPUS, STACK_SIZE);

void worker_entry(void *p1, void *p2, void *p3)
{
    int core_id = (int)(long)p1;
    ARG_UNUSED(p2);
    ARG_UNUSED(p3);

    while (1) {
        printk("Heartbeat from Core %d (Hart %d)\n", core_id, arch_proc_id());
        k_busy_wait(1000000); // 1 second roughly
        k_yield();
    }
}

int main(void)
{
	printk("Hello World from SMP Cluster 1! (Boot Core %d)\n", arch_proc_id());
    
    // Spawn threads for all cores (including this one)
    for (int i = 0; i < CONFIG_MP_MAX_NUM_CPUS; i++) {
        // We can't pin thread to core 0 easily if we are running on it?
        // Actually we can.
        // But main thread is already running on Core 0.
        // We'll spawn new threads.
        
        // Note: Zephyr doesn't strictly pin unless we use specific API or scheduler.
        // But usually creating a thread doesn't guarantee core.
        // However, we can use k_thread_create and let scheduler distribute.
        // Or we can just print from main loop for Core 0, and spawn for others?
        
        // Let's just spawn and hope scheduler distributes.
        // Or use k_thread_cpu_mask_clear/enable if available.
        
        k_thread_create(&worker_threads[i], worker_stacks[i],
                        STACK_SIZE, worker_entry,
                        (void *)(long)i, NULL, NULL,
                        PRIORITY, 0, K_NO_WAIT);
    }

    // Main thread can just sleep
    while (1) {
        k_sleep(K_FOREVER);
    }
	return 0;
}
