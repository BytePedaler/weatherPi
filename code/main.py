import os
import csv
import socket
import traceback
import main_init # idk yet
import main_config # idk yet
import sense_acq # idk yet
import data_comp
from time import localtime, strftime, sleep
from pathlib import Path
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003


# /////////////
# Main Entry
# \\\\\\\\\\\\\
if __name__ == "__main__":
    initialization()
    sensor_acquisition()