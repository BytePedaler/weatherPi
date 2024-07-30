from time import localtime, strftime, sleep

SECONDS_PER_MINUTE = 60

def time_interval():
    min_interval = SECONDS_PER_MINUTE * 0.016667
    return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d, %H, %M, %S", localtime())
    return current_time

def sensor_acquisition():
    while True:
        sensor_timer = strftime("%S", localtime())
        # print("Current timer: " + sensor_timer)
        if sensor_timer == "00":
            print(time_recording())
        elif sensor_timer == "30":
            print(time_recording())
        sleep(time_interval())

if __name__ == '__main__':
    sensor_acquisition()