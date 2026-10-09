
from pathlib import Path
from datetime import datetime
import shutil

BASE = Path(__file__).parent
SOURCE_DIR = BASE / "source_configs"
BACKUP_DIR = BASE / "backups"

# Create the backup folder if it does not exist
BACKUP_DIR.mkdir(parents=True, exist_ok=True)

# Find saved router configurations
config_files = sorted(SOURCE_DIR.glob("*_running_config.txt"))

if not config_files:
    print("No configuration files found!")
    print(f"Add R1_running_config.txt and R2_running_config.txt to {SOURCE_DIR}")
    raise SystemExit(1)

# Create a timestamp for this backup run
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

print("\n===== ROUTER CONFIGURATION BACKUP =====")

for config_file in config_files:
    backup_name = f"{config_file.stem}_{timestamp}.txt"
    backup_path = BACKUP_DIR / backup_name

    try:
        shutil.copy2(config_file, backup_path)
        print(f"BACKUP OK: {config_file.name}")
        print(f"Saved to:  {backup_path}")
    except OSError as error:
        print(f"BACKUP FAILED: {config_file.name}")
        print(f"Reason: {error}")

print("\nBackup process finished.")
