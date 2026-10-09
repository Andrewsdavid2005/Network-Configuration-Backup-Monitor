
import subprocess
import sys
from pathlib import Path

BASE = Path(__file__).parent

scripts = [
    "health_check.py",
    "parse_router_output.py",
    "backup_config.py"
]

print("\n====================================")
print(" NETWORK AUTOMATION TOOLKIT")
print("====================================")

for script in scripts:
    script_path = BASE / script

    print(f"\n\nRunning: {script}")
    print("-" * 40)

    if not script_path.exists():
        print(f"ERROR: {script} not found.")
        continue

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=BASE
    )

    if result.returncode == 0:
        print(f"Completed: {script}")
    else:
        print(f"Check failed: {script} (exit {result.returncode})")

print("\n====================================")
print(" AUTOMATION RUN FINISHED")
print("====================================")
