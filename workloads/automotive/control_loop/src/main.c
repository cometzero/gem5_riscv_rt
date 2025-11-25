/*
 * Automotive Control Loop - Baseline Workload
 * 
 * Periodic control task with 1ms period for automotive simulation
 */

#include <zephyr/kernel.h>
#include <zephyr/sys/printk.h>
#include <zephyr/timing/timing.h>
#include <zephyr/random/random.h>

/* Control task parameters */
#define CONTROL_PERIOD_MS 1
#define CONTROL_STACK_SIZE 2048
#define CONTROL_PRIORITY 5

/* Performance tracking */
#define MAX_ITERATIONS 1100
#define DEADLINE_CYCLES 500000  /* 1ms @ 500MHz */

/* Control state machine */
typedef enum {
	STATE_IDLE,
	STATE_ACTIVE,
	STATE_ERROR
} control_state_t;

/* Timing statistics */
struct timing_stats {
	uint32_t start_cycle;
	uint32_t end_cycle;
	uint32_t response_time;
	uint32_t iteration;
	bool deadline_miss;
};

/* Global state */
static control_state_t state = STATE_IDLE;
static int32_t sensor_value = 0;
static int32_t actuator_value = 0;
static struct timing_stats stats[MAX_ITERATIONS];
static uint32_t iteration_count = 0;
static uint32_t deadline_misses = 0;

/* Timer for periodic control task */
K_TIMER_DEFINE(control_timer, NULL, NULL);

/* Simulated sensor read */
static inline int32_t sensor_read(void)
{
	/* Simple counter simulation */
	return sensor_value++;
}

/* Simulated actuator write */
static inline void actuator_write(int32_t value)
{
	actuator_value = value;
}

/* Simple control algorithm - state machine */
static void control_algorithm(int32_t sensor)
{
	switch (state) {
	case STATE_IDLE:
		if (sensor > 100) {
			state = STATE_ACTIVE;
		}
		actuator_write(0);
		break;

	case STATE_ACTIVE:
		/* Simple proportional control */
		actuator_write(sensor * 2);
		if (sensor > 1000) {
			state = STATE_ERROR;
		}
		break;

	case STATE_ERROR:
		actuator_write(0);
		if (sensor < 50) {
			state = STATE_IDLE;
		}
		break;
	}
}

/* Periodic control task */
static void control_task(void)
{
	uint32_t start, end, response;
	int32_t sensor;

	while (iteration_count < MAX_ITERATIONS) {
		/* Wait for next period */
		k_timer_status_sync(&control_timer);

		/* Measurement point: task start */
		start = k_cycle_get_32();

		/* Read sensor */
		sensor = sensor_read();

		/* Execute control algorithm */
		control_algorithm(sensor);

		/* Measurement point: task end */
		end = k_cycle_get_32();

		/* Calculate response time */
		response = end - start;

		/* Record statistics */
		if (iteration_count < MAX_ITERATIONS) {
			stats[iteration_count].start_cycle = start;
			stats[iteration_count].end_cycle = end;
			stats[iteration_count].response_time = response;
			stats[iteration_count].iteration = iteration_count;
			stats[iteration_count].deadline_miss = (response > DEADLINE_CYCLES);

			if (response > DEADLINE_CYCLES) {
				deadline_misses++;
			}

			/* Log every 100 iterations */
			if (iteration_count % 100 == 0) {
				printk("[CTRL] Iter: %04u, Start: 0x%08x, End: 0x%08x, "
				       "Response: %u cycles, State: %d\n",
				       iteration_count, start, end, response, state);
			}

			iteration_count++;
		}
	}

	/* Print summary */
	printk("\n[CTRL] ===== SUMMARY =====\n");
	printk("[CTRL] Total iterations: %u\n", iteration_count);
	printk("[CTRL] Deadline misses: %u\n", deadline_misses);
	printk("[CTRL] Compliance: %u.%u%%\n",
	       (iteration_count - deadline_misses) * 100 / iteration_count,
	       ((iteration_count - deadline_misses) * 1000 / iteration_count) % 10);
	printk("[CTRL] ==================\n");
}

/* Background monitoring task */
static void monitor_task(void)
{
	while (1) {
		k_sleep(K_MSEC(1000));
		if (iteration_count < MAX_ITERATIONS) {
			printk("[MON] System running, iterations: %u, misses: %u\n",
			       iteration_count, deadline_misses);
		}
	}
}

/* Thread definitions */
K_THREAD_DEFINE(control_tid, CONTROL_STACK_SIZE, control_task, NULL, NULL, NULL,
		CONTROL_PRIORITY, 0, 0);

K_THREAD_DEFINE(monitor_tid, 1024, monitor_task, NULL, NULL, NULL,
		CONTROL_PRIORITY + 5, 0, 0);

int main(void)
{
	printk("\n");
	printk("========================================\n");
	printk("Automotive Control Loop - Baseline\n");
	printk("========================================\n");
	printk("Period: %d ms\n", CONTROL_PERIOD_MS);
	printk("Deadline: %u cycles (@ 500MHz)\n", DEADLINE_CYCLES);
	printk("Target iterations: %u\n", MAX_ITERATIONS);
	printk("========================================\n\n");

	/* Start periodic timer */
	k_timer_start(&control_timer, K_MSEC(CONTROL_PERIOD_MS),
		      K_MSEC(CONTROL_PERIOD_MS));

	printk("[MAIN] Control timer started\n");
	printk("[MAIN] Waiting for completion...\n\n");

	return 0;
}
