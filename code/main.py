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

# Detect directories dynamically
BASE_DIR = path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
LOG_FILE = BASE_DIR / "weatherPi.log"
DATA_DIR.mkdir(exist_ok=True)

# Get device name for data output
current_device_name = socket.gethostname()


# /////////////  
# Config, etc (either obsolete or on its way out)
# \\\\\\\\\\\\\
# Get user name for data output (this is to ensure the correct filepath for the data saves) -- mostly obsolete
current_username = os.getlogin()

# Define the interval for triggering data write (e.g., every 15 seconds)
trigger_interval = 15

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

# File initialization:
with open('/home/' + current_username + '/weatherPi/data/wp_data_1.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['system downtime'])
    csvfile.close()

with open('/home/' + current_username + '/weatherPi/data/wp_data_2.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['system downtime'])
    csvfile.close()

def initialization():
    print("Running Weather Pi")
    print("Currently running on " + current_device_name)
    print("Please remember that the first set of data recorded may be erroneous.")
    print("The sensors often need a few minutes to acclimate!")
    if MODE == 1:
        print("WARNING: DEBUG MODE CURRENTLY ACTIVE")
    elif MODE == 0:
        pass

def sensor_acq_mode():
    if MODE == 0:
        acq_mode = "%M"
        return acq_mode
    elif MODE == 1:
        acq_mode = "%S"
        return acq_mode


# Time recording and collection:
def time_interval():
    if MODE == 0:
        # Real world Collection interval:
        min_interval = SECONDS_PER_MINUTE * 1
        return min_interval
    elif MODE == 1:
        # Debug time interval:
        min_interval = 1
        return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d; %H:%M:%S", localtime())
    return current_time


# Sensor data collection:
def sens_data():
    global file_switch_status
    time_multiplier = (int(time_interval()) * 15)
    global temp_readings
    global humidity_readings
    global pressure_readings
    global light_readings
    temp_readings.clear()
    humidity_readings.clear()
    pressure_readings.clear()
    light_readings.clear()
    for i in range(time_multiplier - 1):
        current_temp = bme280.get_temperature()
        temp_readings.append(current_temp)
        current_humidity = bme280.get_humidity()
        humidity_readings.append(current_humidity)
        current_pressure = bme280.get_pressure()
        pressure_readings.append(current_pressure)
        current_light = ltr.get_lux()
        light_readings.append(current_light)
        sleep(1)
    avg_temp_reading = sum(temp_readings) / len(temp_readings)
    converted_temp = ((float(avg_temp_reading) * 9 / 5) + 32)
    avg_humidity_reading = sum(humidity_readings) / len(humidity_readings)
    avg_pressure_reading = sum(pressure_readings) / len(pressure_readings)
    avg_light_reading = sum(light_readings) / len(light_readings)
    pm_sensor()

    # return avg_temp_reading, converted_temp, avg_humidity_reading, avg_pressure_reading, avg_light_reading

    if file_switch_status == 1:
        with open('/home/' + current_username + '/weatherPi/data/wp_data_1.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            writer.writerow(["New Data: ", time_recording(), current_device_name, avg_temp_reading, converted_temp, avg_humidity_reading,
                             avg_pressure_reading, avg_light_reading, pm_sensor()])
            csvfile.close()
        file_switch_status = 0
    else:
        with open('/home/' + current_username + '/weatherPi/data/wp_data_2.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
            writer.writerow(["New Data: ", time_recording(), current_device_name, avg_temp_reading, converted_temp, avg_humidity_reading,
                             avg_pressure_reading, avg_light_reading, pm_sensor()])
            csvfile.close()
        file_switch_status = 1

def pm_sensor():
    part_mat_readings_raw = pms5003.read()
    part_mat_readings = str(part_mat_readings_raw)
    pm_readings = []
    msm_data_lines = part_mat_readings.split('\n')
    for line in msm_data_lines:
        parts = line.split(":")
        if len(parts) > 1:
            measurement = parts[1].strip()
            pm_readings.append(measurement)
    return pm_readings

# Data recording
# def data_write():
#     with open('wptestfile.csv', 'a', newline='') as csvfile:
#         writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
#         writer.writerow(["New Data: ", time_recording(), sens_data(), pm_sensor()])
#         csvfile.close()

def sensor_acquisition():
    while True:
        # Continuous sensor acquisition
        current_second = int(strftime(sensor_acq_mode(), localtime()))  # Get the current second

        global last_write_time  # Use the global variable to track the last write time

        # Check if it's time to write data (every 15 seconds) and ensure no repeated writes within the same second
        if current_second % trigger_interval == 0 and last_write_time != current_second:
            sensor_readings()
            last_write_time = current_second

# Debug mode only:
def sensor_readings():
    if MODE == 0:
        sens_data()
    elif MODE == 1:
        sens_data()
        print("Current sensor readings for debugging and testing: ")
        print("Current temperature, humidity, pressure, light: " + str(sens_data()))
        # print("Current gas: " + str(gas_readings))
        print("Current particulates: " + str(pm_sensor()))
        print("Data written at: " + time_recording())

def dataWriteFile1():
    with open('/home/' + current_username + '/weatherPi/data/acqtestfile1.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["New Data: ", time_recording(), "Test file 1"])
        csvfile.close()

def dataWriteFile2():
    with open('/home/' + current_username + '/weatherPi/data/acqtestfile2.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["New Data: ", time_recording(), "Test file 2"])
        csvfile.close()


if __name__ == '__main__':
    initialization()
    sensor_acquisition()