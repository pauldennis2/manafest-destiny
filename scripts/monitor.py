import os
import psutil
import time

LIMIT_MB = 12000  # Set memory limit to 12GB

def check_memory():
    mem = psutil.virtual_memory()
    used_mb = mem.used / (1024 * 1024)

    if used_mb > LIMIT_MB:
        print(f"Memory usage exceeded ({used_mb:.1f}MB). Terminating all Python processes.")
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            if "python" in proc.info['name'].lower():
                os.kill(proc.info['pid'], 9)  # Kill process forcefully

while True:
    check_memory()
    time.sleep(1)  # Adjust monitoring frequency if needed
