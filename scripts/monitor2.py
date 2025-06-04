import os
import psutil
import time

LIMIT_MB = 12000  # Set memory limit to 12GB

# Get the monitoring script’s PID to avoid self-termination
monitor_pid = os.getpid()

def check_memory():
    mem = psutil.virtual_memory()
    used_mb = mem.used / (1024 * 1024)

    if used_mb > LIMIT_MB:
        print(f"Memory usage exceeded ({used_mb:.1f}MB). Identifying highest memory-consuming Python process...")

        highest_mem_proc = None
        highest_mem_usage = 0

        # Find the worst offender (largest memory-consuming Python process)
        for proc in psutil.process_iter(attrs=['pid', 'name', 'memory_info']):
            if "python" in proc.info['name'].lower() and proc.info['pid'] != monitor_pid:
                mem_usage = proc.info['memory_info'].rss  # Resident memory usage in bytes
                if mem_usage > highest_mem_usage:
                    highest_mem_usage = mem_usage
                    highest_mem_proc = proc

        if highest_mem_proc:
            print(f"Terminating Python process {highest_mem_proc.info['pid']} using {highest_mem_usage / (1024 * 1024):.1f}MB")
            os.kill(highest_mem_proc.info['pid'], 9)  # Force kill the worst offender
            time.sleep(0.5)  # Brief pause to ensure termination before continuing

while True:
    check_memory()
    time.sleep(1)  # Adjust monitoring frequency if needed
