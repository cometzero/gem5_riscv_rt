# Automotive Baseline Workload Specification

## Overview

This document defines the automotive baseline workload for the gem5 RISC-V full-system simulation. The workload implements a periodic control loop representative of automotive real-time systems.

## Workload Structure

### 1. Periodic Control Task

**Purpose**: Main control loop for automotive system (e.g., engine control, ABS, steering)

**Characteristics**:
- **Period**: 1 ms (1000 Hz)
- **Deadline**: 1 ms (hard real-time)
- **Priority**: High (real-time priority)
- **Execution Pattern**: Periodic, synchronized with timer

**Operations**:
1. Read sensor data (simulated)
2. Execute control algorithm (PID or state machine)
3. Write actuator commands (simulated)
4. Log timing information

### 2. Background Monitoring Task

**Purpose**: System health monitoring, diagnostics

**Characteristics**:
- **Period**: Best-effort (non-periodic)
- **Priority**: Low (background)
- **Execution Pattern**: Runs when CPU is idle

**Operations**:
- Monitor system status
- Log diagnostic information
- Non-critical operations

### 3. Simulated Sensor ISR

**Purpose**: Interrupt service routine for sensor data acquisition

**Characteristics**:
- **Trigger**: Timer interrupt every 1 ms
- **Latency Requirement**: < 100 μs
- **Priority**: Highest (interrupt level)

**Operations**:
- Acknowledge interrupt
- Read sensor data
- Wake up control task

## Control Algorithm

### Simple State Machine (Baseline)

```c
typedef enum {
    STATE_IDLE,
    STATE_ACTIVE,
    STATE_ERROR
} control_state_t;

control_state_t state = STATE_IDLE;
int32_t sensor_value = 0;
int32_t actuator_value = 0;

void control_algorithm(void) {
    // Read sensor (simulated with counter)
    sensor_value++;
    
    // Simple state machine
    switch (state) {
        case STATE_IDLE:
            if (sensor_value > 100) {
                state = STATE_ACTIVE;
            }
            actuator_value = 0;
            break;
            
        case STATE_ACTIVE:
            // Simple proportional control
            actuator_value = sensor_value * 2;
            if (sensor_value > 1000) {
                state = STATE_ERROR;
            }
            break;
            
        case STATE_ERROR:
            actuator_value = 0;
            if (sensor_value < 50) {
                state = STATE_IDLE;
            }
            break;
    }
}
```

### PID Controller (Alternative)

```c
typedef struct {
    float kp;  // Proportional gain
    float ki;  // Integral gain
    float kd;  // Derivative gain
    float prev_error;
    float integral;
} pid_controller_t;

float pid_update(pid_controller_t *pid, float setpoint, float measurement) {
    float error = setpoint - measurement;
    pid->integral += error;
    float derivative = error - pid->prev_error;
    pid->prev_error = error;
    
    return (pid->kp * error) + (pid->ki * pid->integral) + (pid->kd * derivative);
}
```

## Timing Measurement Points

### 1. Task Start Timestamp
- **Measurement**: `k_cycle_get_32()` at beginning of control_task()
- **Purpose**: Calculate inter-arrival time and response time

### 2. Task End Timestamp
- **Measurement**: `k_cycle_get_32()` at end of control_task()
- **Purpose**: Calculate execution time and response time

### 3. ISR Latency
- **Measurement**: Time from interrupt trigger to ISR entry
- **Purpose**: Verify interrupt response time

## Performance Metrics

### Success Criteria

1. **Iteration Count**: >= 1000 task completions
2. **Deadline Compliance**: >= 95% (< 50 misses out of 1000)
3. **Period Accuracy**: Inter-arrival time = 1ms ± 5%
4. **Response Time**: < 1ms for 95% of iterations

### Timing Calculations

**Response Time** = Task End Timestamp - Task Start Timestamp

**Inter-Arrival Time** = Task Start Timestamp[i+1] - Task Start Timestamp[i]

**Deadline Miss** = Response Time > 1ms (500,000 cycles @ 500 MHz)

**Miss Rate** = (Number of Misses / Total Iterations) * 100%

## Implementation Notes

### Zephyr RTOS Configuration

Required Kconfig options:
- `CONFIG_PRINTK=y` - Enable printf-style logging
- `CONFIG_TIMERS=y` - Enable kernel timers
- `CONFIG_TIMING_FUNCTIONS=y` - Enable timing measurement
- `CONFIG_SYS_CLOCK_TICKS_PER_SEC=1000` - 1ms tick resolution

### gem5 Simulation Configuration

- **CPU Frequency**: 500 MHz
- **Simulated Time**: >= 1 second (for 1000 iterations @ 1ms)
- **Memory**: 128 MB DRAM
- **Cache**: L1 I/D 32KB, L2 256KB

### Output Format

```
[CTRL] Iteration: 0001, Start: 0x00012345, End: 0x00012678, Response: 819 cycles
[CTRL] Iteration: 0002, Start: 0x000623ab, End: 0x000626de, Response: 819 cycles
...
[CTRL] Summary: 1000 iterations, 12 misses, 98.8% compliance
```

## Directory Structure

```
workloads/automotive/control_loop/
├── src/
│   └── main.c           # Main control loop implementation
├── CMakeLists.txt       # Zephyr build configuration
├── prj.conf             # Zephyr project configuration
└── README.md            # Workload documentation
```

## References

- Zephyr RTOS Timer API: https://docs.zephyrproject.org/latest/kernel/services/timing/timers.html
- Zephyr Timing Functions: https://docs.zephyrproject.org/latest/kernel/services/timing/clocks.html
- gem5 Statistics: https://www.gem5.org/documentation/general_docs/statistics/
