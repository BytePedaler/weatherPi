import os # idk yet
import socket
from pathlib import Path


# /////////////
# Config
# \\\\\\\\\\\\\
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


# /////////////
# Config, etc (either obsolete or on its way out)
# \\\\\\\\\\\\\
# Get user name for data output (this is to ensure the correct filepath for the data saves) -- mostly obsolete
# USERNAME = os.getlogin()

# Const variables:
temp_readings = []
pressure_readings = []
humidity_readings = []
light_readings = []

# Additional variables:
file_switch_status = 1
last_write_time = None