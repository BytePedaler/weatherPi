from time import localtime, strftime, sleep
import csv
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003

# Const:
SECONDS_PER_MINUTE = 60

# Sensor initialization:
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()
pms5003 = PMS5003()
current_temp = bme280.get_temperature()
converted_temp = ((float(current_temp) * 9/5) + 32)
current_pressure = bme280.get_pressure()
current_humidity = bme280.get_humidity()
current_light = ltr.get_lux()
# gas_readings = gas.read_all()
part_mat_readings_raw = pms5003.read()
part_mat_readings = str(part_mat_readings_raw)

# Particulate sensor data:
def pm_data():
    pm_readings = []
    msm_data_lines = part_mat_readings.split('\n')
    for line in msm_data_lines:
        parts = line.split(":")
        if len(parts) > 1:
            measurement = parts[1].strip()
            pm_readings.append(measurement)
    return(pm_readings)

# File initialization:
with open('wptestfile.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['system downtime'])
    csvfile.close()

def data_write():
    with open('wptestfile.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(["New Data: ", time_recording(), current_temp, converted_temp, current_pressure, current_humidity, current_light, pm_data()])
        csvfile.close()

def time_interval():
     min_interval = SECONDS_PER_MINUTE * 0.016667
     return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d, %H, %M, %S", localtime())
    return current_time

def sensor_readings():
    print("Current sensor readings for debugging and testing: ")
    print("Current temperature: " + str(current_temp))
    print("Current pressure: " + str(current_pressure))
    print("Current humidity: " + str(current_humidity))
    print("Current light level: " + str(current_light))
    # print("Current gas: " + str(gas_readings))
    print("Current particulates: " + str(part_mat_readings))

def sensor_acquisition():
    while True:
        sensor_timer = strftime("%S", localtime())
        # print("Current timer: " + sensor_timer)
        if sensor_timer == "00":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
        elif sensor_timer == "30":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
        sleep(time_interval())


if __name__ == '__main__':
    sensor_acquisition()