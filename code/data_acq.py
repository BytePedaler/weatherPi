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
# Acquisition Loop
# \\\\\\\\\\\\\
def sensor_acquisition():
    file_switch = 1
    last_write_time = None
    while True:
        try:
            current_second = int(strftime("%S" if MODE else "%M", localtime()))
            if current_second % TRIGGER_INTERVAL == 0 and last_write_time != current_second:
                data = sens_data()
                write_data(file_switch, ["New Data:"] + data)
                log(f"Data written: {data}")
                file_switch = 1 - file_switch  # alternate files
                last_write_time = current_second
        except Exception as e:
            log("Error: " + str(e))
            log(traceback.format_exc())
            sleep(5)  # Prevent crash loop