import csv
import socket
import main_config
from time import localtime, strftime, sleep
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003


# /////////////
# Init
# \\\\\\\\\\\\\
# Sensor initialization:
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()
pms5003 = PMS5003()
# gas_readings = gas.read_all() # still in testing

def log(msg):
    """Log messages to file with timestamp."""
    with open(LOG_FILE, "a") as log_file:
        log_file.write(f"[{strftime('%Y-%m-%d %H:%M:%S')}] {msg}\n")

def initialization():
    print("Running Weather Pi")
    print(f"Currently running on {DEVICE_NAME}")
    print("Please remember that the first set of data recorded may be erroneous. The sensors often need a few minutes to acclimate!")
    if MODE == 1:
        print("WARNING: DEBUG MODE CURRENTLY ACTIVE")
    elif MODE == 0:
        pass