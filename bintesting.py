from time import localtime, strftime, sleep

SECONDS_PER_MINUTE = 60
switch_status = 0

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
            func_switch()
            print(time_recording())
            print(func_switch())
        elif sensor_timer == "30":
            func_switch()
            print(time_recording())
            print(func_switch())
        sleep(time_interval())

def func_switch():
    if switch_status == 0:
        switch_status = 1
        return switch_status
    else:
        switch_status = 0
        return switch_status

def main():
    sensor_acquisition()

if __name__ == '__main__':
    main()