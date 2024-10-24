from time import localtime, strftime, sleep
import time
import csv

file_switch_status = 1

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
    sensor_timer = strftime(sensor_acq_mode(), localtime()) # Real world collection time
    if sensor_timer == "00":
        dataAcquisition()
        # data_write()
    elif sensor_timer == "15":
        dataAcquisition()
        # data_write()
    elif sensor_timer == "30":
        dataAcquisition()
        # data_write()
    elif sensor_timer == "45":
        dataAcquisition()
        # data_write()


# New code below:



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
    time_multiplier = (int(time_interval()) * 15)
    if file_switch_status == 1:
        print(file_switch_status)
        FILE_SWITCH = file_switch_status - 1
        dataWriteFile1()
    else:
        print(file_switch_status)
        FILE_SWITCH = file_switch_status + 1
        dataWriteFile2()



if __name__ == '__main__':
    while True:
        sensor_acquisition()