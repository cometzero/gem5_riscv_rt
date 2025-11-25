#!/usr/bin/env python3
"""
Post-processing script for gem5 RISC-V RT baseline experiments.
Extracts performance metrics from gem5 stats and Zephyr logs.
"""

import argparse
import csv
import os
import re
import sys
from pathlib import Path

def parse_gem5_stats(stats_file):
    """Extract metrics from gem5 stats.txt"""
    metrics = {
        'ipc': 0.0,
        'l1i_miss_rate': 0.0,
        'l1d_miss_rate': 0.0,
        'l2_miss_rate': 0.0,
        'mem_latency': 0.0
    }
    
    if not os.path.exists(stats_file):
        print(f"Warning: Stats file not found: {stats_file}")
        return metrics

    with open(stats_file, 'r') as f:
        content = f.read()
        
        # Extract IPC
        ipc_match = re.search(r'system\.cpu\.ipc\s+([0-9\.]+)', content)
        if ipc_match:
            metrics['ipc'] = float(ipc_match.group(1))
            
        # Extract L1 I-Cache Miss Rate
        l1i_match = re.search(r'system\.cpu\.icache\.overallMissRate::total\s+([0-9\.]+)', content)
        if l1i_match:
            metrics['l1i_miss_rate'] = float(l1i_match.group(1))
            
        # Extract L1 D-Cache Miss Rate
        l1d_match = re.search(r'system\.cpu\.dcache\.overallMissRate::total\s+([0-9\.]+)', content)
        if l1d_match:
            metrics['l1d_miss_rate'] = float(l1d_match.group(1))
            
        # Extract L2 Cache Miss Rate
        l2_match = re.search(r'system\.l2cache\.overallMissRate::total\s+([0-9\.]+)', content)
        if l2_match:
            metrics['l2_miss_rate'] = float(l2_match.group(1))
            
        # Extract Memory Latency (average)
        # Note: gem5 stats might vary, looking for dram controller stats
        mem_lat_match = re.search(r'system\.mem_ctrl\.dram\.avgReadLatency\s+([0-9\.]+)', content)
        if mem_lat_match:
            metrics['mem_latency'] = float(mem_lat_match.group(1))
            
    return metrics

def parse_zephyr_log(log_file):
    """Extract task timing from Zephyr terminal output"""
    metrics = {
        'avg_response_time': 0.0,
        'max_response_time': 0.0,
        'deadline_misses': 0,
        'iterations': 0
    }
    
    if not os.path.exists(log_file):
        print(f"Warning: Log file not found: {log_file}")
        return metrics
        
    response_times = []
    
    with open(log_file, 'r') as f:
        for line in f:
            # Look for [CTRL] lines
            # [CTRL] Iter: 0000, Start: 0x0000c562, End: 0x0000c598, Response: 54 cycles, State: 0
            match = re.search(r'\[CTRL\] Iter: (\d+),.*Response: (\d+) cycles', line)
            if match:
                response = int(match.group(2))
                response_times.append(response)
                
            # Look for summary lines
            # [CTRL] Deadline misses: 0
            miss_match = re.search(r'\[CTRL\] Deadline misses: (\d+)', line)
            if miss_match:
                metrics['deadline_misses'] = int(miss_match.group(1))
                
    if response_times:
        metrics['iterations'] = len(response_times)
        metrics['avg_response_time'] = sum(response_times) / len(response_times)
        metrics['max_response_time'] = max(response_times)
        
    return metrics

def main():
    parser = argparse.ArgumentParser(description='Post-process gem5 simulation results')
    parser.add_argument('--input-dir', required=True, help='Input directory containing simulation results')
    parser.add_argument('--output-csv', default='docs/results/baseline_summary.csv', help='Output CSV file')
    args = parser.parse_args()
    
    results_dir = Path(args.input_dir)
    if not results_dir.exists():
        print(f"Error: Input directory {results_dir} does not exist")
        sys.exit(1)
        
    # Prepare CSV output
    csv_headers = [
        'Config', 'Workload', 
        'IPC', 'L1I_Miss', 'L1D_Miss', 'L2_Miss', 'Mem_Latency',
        'Avg_Response', 'Max_Response', 'Deadline_Misses', 'Iterations'
    ]
    
    rows = []
    
    # Walk through results directory
    # Structure: results/CONFIG/WORKLOAD/
    for config_dir in results_dir.iterdir():
        if not config_dir.is_dir():
            continue
            
        config_name = config_dir.name
        
        for workload_dir in config_dir.iterdir():
            if not workload_dir.is_dir():
                continue
                
            workload_name = workload_dir.name
            print(f"Processing {config_name}/{workload_name}...")
            
            stats_file = workload_dir / 'stats.txt'
            log_file = workload_dir / 'system.platform.terminal'
            
            gem5_metrics = parse_gem5_stats(stats_file)
            zephyr_metrics = parse_zephyr_log(log_file)
            
            row = {
                'Config': config_name,
                'Workload': workload_name,
                'IPC': f"{gem5_metrics['ipc']:.4f}",
                'L1I_Miss': f"{gem5_metrics['l1i_miss_rate']:.6f}",
                'L1D_Miss': f"{gem5_metrics['l1d_miss_rate']:.6f}",
                'L2_Miss': f"{gem5_metrics['l2_miss_rate']:.6f}",
                'Mem_Latency': f"{gem5_metrics['mem_latency']:.2f}",
                'Avg_Response': f"{zephyr_metrics['avg_response_time']:.2f}",
                'Max_Response': f"{zephyr_metrics['max_response_time']:.2f}",
                'Deadline_Misses': zephyr_metrics['deadline_misses'],
                'Iterations': zephyr_metrics['iterations']
            }
            rows.append(row)
            
    # Write to CSV
    os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
    with open(args.output_csv, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        writer.writerows(rows)
        
    print(f"Results written to {args.output_csv}")

if __name__ == '__main__':
    main()
