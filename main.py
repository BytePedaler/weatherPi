from time import localtime, strftime, sleep
import time
import csv
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
# import gas
from pms5003 import PMS5003

# Const:
SECONDS_PER_MINUTE = 60
# For debugging only:
# SECONDS_PER_MINUTE = 0.016667

# Sensor initialization:
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()
pms5003 = PMS5003()
# gas_readings = gas.read_all()


def initialization():
    print("Running Weather Pi")

# Particulate sensor data:
def pm_data():
    part_mat_readings_raw = pms5003.read()
    part_mat_readings = str(part_mat_readings_raw)
    pm_readings = []
    msm_data_lines = part_mat_readings.split('\n')
    for line in msm_data_lines:
        parts = line.split(":")
        if len(parts) > 1:
            measurement = parts[1].strip()
            pm_readings.append(measurement)
    return(pm_readings)

# Temperature sensor data:
def temp_data():
    temp_readings = []
    pressure_readings = []
    humidity_readings = []
    light_readings = []
    for i in range(10):
        current_temp = bme280.get_temperature()
        current_pressure = bme280.get_pressure()
        current_humidity = bme280.get_humidity()
        current_light = ltr.get_lux()
        temp_readings.append(current_temp)
        pressure_readings.append(current_pressure)
        humidity_readings.append(current_humidity)
        light_readings.append(current_light)
        # print(len(temp_readings))
    # print(len(temp_readings))
    avg_temp_reading = sum(temp_readings) / len(temp_readings)
    avg_pressure_reading = sum(pressure_readings) / len(pressure_readings)
    avg_humidity_reading = sum(humidity_readings) / len(humidity_readings)
    avg_light_reading = sum(light_readings) / len(light_readings)
    converted_temp = ((float(avg_temp_reading) * 9 / 5) + 32)
    # print("Current temperature: " + str(avg_temp_reading) + " or " + str(converted_temp))
    return(avg_temp_reading, converted_temp, avg_pressure_reading, avg_humidity_reading, avg_light_reading)


# File initialization:
with open('wptestfile.csv', 'a', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['system downtime'])
    csvfile.close()

def data_write():
    with open('wptestfile.csv', 'a', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator='\n')
        writer.writerow(["New Data: ", time_recording(), temp_data(), pm_data()])
        csvfile.close()

def time_interval():
    # Debug time interval:
    # min_interval = SECONDS_PER_MINUTE * 0.016667
    # Real world Collection interval:
    min_interval = SECONDS_PER_MINUTE * 1
    return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d, %H, %M, %S", localtime())
    return current_time

# def sensor_readings():
#     print("Current sensor readings for debugging and testing: ")
#     print("Current temperature: " + str(current_temp))
#     print("Current pressure: " + str(current_pressure))
#     print("Current humidity: " + str(current_humidity))
#     print("Current light level: " + str(current_light))
#     print("Current gas: " + str(gas_readings))
#     print("Current particulates: " + str(part_mat_readings))

def sensor_acquisition():
    while True:
        temp_data()
        # Debug time:
        # sensor_timer = strftime("%S", localtime())
        # Real world collection time:
        sensor_timer = strftime("%M", localtime())
        # print("Current timer: " + sensor_timer)
        if sensor_timer == "00":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
            time.sleep(60)
        elif sensor_timer == "15":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
            time.sleep(60)
        elif sensor_timer == "30":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
            time.sleep(60)
        elif sensor_timer == "45":
            # print("Data written at: " + time_recording())
            data_write()
            # sensor_readings()
            time.sleep(60)
        sleep(time_interval())


if __name__ == '__main__':
    initialization()
    sensor_acquisition()