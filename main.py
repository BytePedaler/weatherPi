import time
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


def time_interval():
     min_interval = SECONDS_PER_MINUTE * 0.5
     return min_interval

def sensor_readings():
    print("Current temperature: " + str(current_temp))
    print("Current pressure: " + str(current_pressure))
    print("Current humidity: " + str(current_humidity))
    print("Current light level: " + str(current_light))
    print("Current gas: " + str(gas_readings))
    print("Current particulates: " + str(part_mat_readings))

def sensor_acquisition():
    while True:
        sensor_readings()
        # Time:
        print(time.localtime())
        time.sleep(time_interval())


if __name__ == '__main__':
    sensor_acquisition()