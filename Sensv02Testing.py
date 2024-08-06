from time import localtime, strftime, sleep

# Const:
SECONDS_PER_MINUTE = 60

time_data = []

def time_interval():
    # Real world Collection interval:
    min_interval = SECONDS_PER_MINUTE * 0.016667
    return min_interval

def time_recording():
    global time_data
    time_data.clear()
    while True:
        current_time = strftime("%H, %M, %S", localtime())
        print("Current time: " + current_time)
        time_data.append(current_time)
        sleep(time_interval())
    data_len = len(time_data)
    print(str(data_len))

def sensor_acquisition():
    while True:
        sensor_timer = strftime("%S", localtime())
        if sensor_timer == "00":
            time_recording()
        elif sensor_timer == "15":
            time_recording()
        elif sensor_timer == "30":
            time_recording()
        elif sensor_timer == "45":
            time_recording()

if __name__ == '__main__':
    sensor_acquisition()