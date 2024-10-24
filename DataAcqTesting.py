from time import localtime, strftime, sleep
import time
import csv

file_switch_status = 1
last_write_time = None

# Mode selection:
# Normal = 0, Debug = 1
MODE = 1

SECONDS_PER_MINUTE = 60



def time_interval():
    if MODE == 0:
        # Real world Collection interval:
        min_interval = SECONDS_PER_MINUTE * 1
        return min_interval
    elif MODE == 1:
        # Debug time interval:
        min_interval = 1
        return min_interval

def time_recording():
    current_time = strftime("%Y, %m, %d; %H:%M:%S", localtime())
    return current_time

def sensor_acq_mode():
    if MODE == 0:
        acq_mode = "%M"
        return acq_mode
    elif MODE == 1:
        acq_mode = "%S"
        return acq_mode


def sensor_acquisition():
    # Continuous sensor acquisition
    current_second = int(strftime(sensor_acq_mode(), localtime()))  # Get the current second
    trigger_interval = 15  # Define the interval for triggering data write (e.g., every 15 seconds)

    global last_write_time  # Use the global variable to track the last write time

    # Check if it's time to write data (every 15 seconds) and ensure no repeated writes within the same second
    if current_second % trigger_interval == 0 and last_write_time != current_second:
        dataAcquisition()
        last_write_time = current_second  # Update last write time to the current second

# Code barrier for implementation changes: DO NOT REMOVE.



def dataWriteFile1():
    with open('acqtestfile1.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["New Data: ", time_recording(), "Test file 1"])
        csvfile.close()

def dataWriteFile2():
    with open('acqtestfile2.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(["New Data: ", time_recording(), "Test file 2"])
        csvfile.close()


def dataAcquisition():
    global file_switch_status
    print(file_switch_status)

    if file_switch_status == 1:
        dataWriteFile1()
        file_switch_status = 0
    else:
        dataWriteFile2()
        file_switch_status = 1

if __name__ == '__main__':
    while True:
        sensor_acquisition()