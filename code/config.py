import socket
from pathlib import Path


# Mode selection:
MODE = 0 # Normal = 0, Debug = 1
SECONDS_PER_MINUTE = 60
# Define the interval for triggering data write (e.g., every 15 seconds)
TRIGGER_INTERVAL = 15

# Detect directories dynamically
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = BASE_DIR / "weatherPi.log"
DATA_DIR.mkdir(exist_ok=True)

# Get device name for data output
DEVICE_NAME = socket.gethostname()