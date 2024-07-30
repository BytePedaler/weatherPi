from time import localtime, strftime, sleep
import csv
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
from enviroplus import gas
from pms5003 import PMS5003

# Const:
SECONDS_PER_MINUTE = 60

# Sensor initialization:
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()
pms5003 = PMS5003()
current_temp = bme280.get_temperature()
current_pressure = bme280.get_pressure()
current_humidity = bme280.get_humidity()
current_light = ltr.get_lux()
gas_readings = gas.read_all()
part_mat_readings = pms5003.read()

# File initialization:
with open('wptestfile.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['downtime'])

def data_write():
    with open('wptestfile.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow([time_recording(), current_temp, current_pressure, current_humidity, current_light, gas_readings, part_mat_readings])
        # NEED TO CLOSE CSV FILE WHEN FINISHED WRITING EACH TIME

def time_interval():
     min_interval = SECONDS_PER_MINUTE * 0.016667
     return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d, %H, %M, %S", localtime())
    return current_time

def sensor_readings():
    print("Current temperature: " + str(current_temp))
    print("Current pressure: " + str(current_pressure))
    print("Current humidity: " + str(current_humidity))
    print("Current light level: " + str(current_light))
    print("Current gas: " + str(gas_readings))
    print("Current particulates: " + str(part_mat_readings))

def sensor_acquisition():
    while True:
        # Temp for testing:
        # sensor_readings()

        sensor_timer = strftime("%S", localtime())
        # print("Current timer: " + sensor_timer)
        if sensor_timer == "00":
            print(time_recording())
            data_write()
        elif sensor_timer == "30":
            print(time_recording())
            data_write()
        sleep(time_interval())


if __name__ == '__main__':
    sensor_acquisition()