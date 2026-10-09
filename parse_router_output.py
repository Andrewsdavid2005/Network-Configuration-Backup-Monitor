
from pathlib import Path

# Find the project folder
BASE = Path(__file__).parent

# Find the saved router output
file_path = BASE / "sample_outputs" / "R1_interfaces.txt"

print("===== ROUTER INTERFACE ANALYZER =====")

if not file_path.exists():
    print("ERROR: R1_interfaces.txt was not found.")
else:
    lines = file_path.read_text(encoding="utf-8").splitlines()

    for line in lines:
        parts = line.split()

        # Skip empty lines and the column heading
        if not parts or parts[0] == "Interface":
            continue

        # Skip lines that do not contain interface information
        if len(parts) < 6:
            continue

        interface = parts[0]
        ip_address = parts[1]
        status = parts[-2]
        protocol = parts[-1]

        if status.lower() == "up" and protocol.lower() == "up":
            print(f"OK: {interface} is working")
        else:
            print(
                f"WARNING: {interface} is not working properly "
                f"(Status={status}, Protocol={protocol})"
            )
