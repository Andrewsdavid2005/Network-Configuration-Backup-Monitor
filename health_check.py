
import json
import csv
import platform
import subprocess
from datetime import datetime
from pathlib import Path

# Project directory
BASE = Path(__file__).parent

# Load device inventory
with open(BASE / "inventory.json", encoding="utf-8") as f:
    devices = json.load(f)["devices"]

# Store device check results
results = []

print("\n===== NETWORK HEALTH CHECK =====\n")

# Check each device
for device in devices:
    name = device["name"]
    ip = device["ip"]

    flag = "-n" if platform.system() == "Windows" else "-c"

    try:
        result = subprocess.run(
            ["ping", flag, "1", ip],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3
        )

        status = "UP" if result.returncode == 0 else "DOWN"

    except (subprocess.TimeoutExpired, OSError):
        status = "DOWN"

    timestamp = datetime.now().isoformat(timespec="seconds")

    print(f"{name:<10} {ip:<18} {status}")

    # IMPORTANT: Store each result
    results.append([
        timestamp,
        name,
        ip,
        status
    ])

# Calculate summary
up_count = sum(1 for row in results if row[3] == "UP")
down_count = sum(1 for row in results if row[3] == "DOWN")

print("\n===== NETWORK HEALTH SUMMARY =====")
print(f"Total devices checked: {len(results)}")
print(f"Devices UP:            {up_count}")
print(f"Devices DOWN:          {down_count}")

if down_count > 0:
    print("Result: Some devices are unreachable.")
else:
    print("Result: All monitored devices are reachable.")

# Save results to CSV
report = BASE / "network_report.csv"
write_header = not report.exists() or report.stat().st_size == 0

try:
    with open(report, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        if write_header:
            writer.writerow([
                "Timestamp",
                "Device",
                "IP",
                "Status"
            ])

        writer.writerows(results)

    print(f"\nReport saved successfully: {report}")

except OSError as error:
    print(f"\nCould not save report: {error}")
