
from pathlib import Path
from datetime import datetime

BASE = Path(__file__).parent
OUTPUT_DIR = BASE / "sample_outputs"
BACKUP_DIR = BASE / "backups"

report_path = BASE / "automation_summary.txt"
lines = []

lines.append("NETWORK AUTOMATION SUMMARY")
lines.append("=" * 35)
lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}")
lines.append("")

# Analyze saved router interface outputs
lines.append("INTERFACE STATUS")
lines.append("-" * 35)

files = sorted(OUTPUT_DIR.glob("*_interfaces.txt"))

for file in files:
    lines.append(f"\nRouter output: {file.name}")

    for line in file.read_text(encoding="utf-8").splitlines():
        parts = line.split()

        if not parts or parts[0] == "Interface" or len(parts) < 6:
            continue

        interface = parts[0]
        status = parts[-2]
        protocol = parts[-1]

        if status.lower() == "up" and protocol.lower() == "up":
            lines.append(f"OK: {interface} is up/up")
        else:
            lines.append(
                f"WARNING: {interface} status={status}, protocol={protocol}"
            )

# List saved configuration backups
lines.append("\n\nCONFIGURATION BACKUPS")
lines.append("-" * 35)

backups = sorted(BACKUP_DIR.glob("*.txt"))

if backups:
    for backup in backups:
        lines.append(f"{backup.name} ({backup.stat().st_size} bytes)")
else:
    lines.append("No backups found.")

lines.append("\nNote: Interface findings are based on saved CLI output.")
lines.append("Backup files are copies of saved configuration text.")

report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

print("\n".join(lines))
print(f"\nReport saved to: {report_path}")
