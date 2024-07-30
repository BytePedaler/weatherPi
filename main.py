import time
from smbus2 import SMBus
from bme280 import BME280
from ltr559 import LTR559
from enviroplus import gas
from pms5003 import PMS5003

# Const:
SECONDS_PER_MINUTE = 60

# Sensors:
bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)
ltr = LTR559()
gas_readings = gas.read_all()
pms5003 = PMS5003()
part_mat_readings = pms5003.read()


def time_interval():
     min_interval = SECONDS_PER_MINUTE * 0.5
     return min_interval

def sensor_acquisition():
    while True:
        # Sensors:
        print(bme280.get_pressure())
        print(bme280.get_humidity())
        print(ltr.get_lux())
        print(gas_readings)
        print(part_mat_readings)

        # Time:
        print(time.localtime())
        time.sleep(time_interval())


if __name__ == '__main__':
    sensor_acquisition()