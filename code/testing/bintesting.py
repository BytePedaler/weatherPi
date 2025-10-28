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
        switch_status = 0
        sensor_timer = strftime("%S", localtime())
        # print("Current timer: " + sensor_timer)
        if sensor_timer == "00":
            switch_status = 0
            print(time_recording())
            print(switch_status)
        elif sensor_timer == "30":
            switch_status = 1
            print(time_recording())
            print(switch_status)
        sleep(time_interval())


def main():
    sensor_acquisition()

if __name__ == '__main__':
    main()