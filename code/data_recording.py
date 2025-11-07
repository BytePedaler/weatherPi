import os
import csv
import socket
import traceback
from time import localtime, strftime, sleep
from pathlib import Path
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003

# /////////////
# Data Recording, Output 
# \\\\\\\\\\\\\
def write_data(file_num, data):
    csv_path = DATA_DIR / f"wp_data_{file_num}.csv"
    with open(csv_path, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)