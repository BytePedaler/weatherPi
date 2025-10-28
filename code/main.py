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



# /////////////
# Sensor Reading
# \\\\\\\\\\\\\
# Time recording and collection:
def time_recording():
    return strftime("%Y, %m, %d; %H:%M:%S", localtime())

def time_interval():
    return SECONDS_PER_MINUTE if MODE == 0 else 1

# Sensor data collection:
def pm_sensor():
    part_mat_readings_raw = pms5003.read()
    pm_lines = str(part_mat_readings_raw).split('\n')
    pm_readings = []
    for line in pm_lines:
        if ":" in line:
            pm_readings.append(line.split(":")[1].strip())
    return pm_readings

def sens_data():
    temp_list, humidity_list, pressure_list, light_list = [], [], [], []
    time_multiplier = time_interval() * 15

    for _ in range(time_multiplier):
        temp_list.append(bme280.get_temperature())
        humidity_list.append(bme280.get_humidity())
        pressure_list.append(bme280.get_pressure())
        light_list.append(ltr.get_lux())
        sleep(1)

    avg_temp_c = sum(temp_list) / len(temp_list)
    avg_temp_f = (avg_temp_c * 9 / 5) + 32
    avg_humidity = sum(humidity_list) / len(humidity_list)
    avg_pressure = sum(pressure_list) / len(pressure_list)
    avg_light = sum(light_list) / len(light_list)
    pm_values = pm_sensor()

    return [time_recording(), DEVICE_NAME, avg_temp_c, avg_temp_f,
            avg_humidity, avg_pressure, avg_light, pm_values]



# /////////////
# Data Recording, Output 
# \\\\\\\\\\\\\
def write_data(file_num, data):
    csv_path = DATA_DIR / f"wp_data_{file_num}.csv"
    with open(csv_path, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)



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



# /////////////
# Main Entry
# \\\\\\\\\\\\\
if __name__ == "__main__":
    initialization()
    sensor_acquisition()