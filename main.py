import time
SECONDS_PER_MINUTE = 60

def time_interval():
     min_interval = SECONDS_PER_MINUTE * 0.5
     return min_interval

def sensor_acquisition():
    while True:
        print(time.localtime())
        time.sleep(time_interval())

if __name__ == '__main__':
    sensor_acquisition()