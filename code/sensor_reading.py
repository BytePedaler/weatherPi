from config import SECONDS_PER_MINUTE, DEVICE_NAME, MODE
#import init # Testing for obsolete

from time import localtime, strftime, sleep
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003


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