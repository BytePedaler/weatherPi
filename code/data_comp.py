import csv
import traceback
from time import localtime, strftime, sleep
from config import DATA_DIR, MODE, TRIGGER_INTERVAL
from init import log
from sense_acq import sens_data


# /////////////
# Data Recording, Output 
# \\\\\\\\\\\\\
def write_data(file_num, data):
    csv_path = DATA_DIR / f"wp_data_{file_num}.csv"
    with open(csv_path, "a", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(data)


# /////////////
# Acquisition Loop
# \\\\\\\\\\\\\
def sensor_acquisition():
    file_switch = 1
    last_write_time = None
    while True:
        try:
            current_second = int(strftime("%S" if MODE else "%M", localtime()))
            if current_second % TRIGGER_INTERVAL == 0 and last_write_time != current_second:
                data = sens_data()
                write_data(file_switch, ["New Data:"] + data)
                log(f"Data written: {data}")
                file_switch = 1 - file_switch  # alternate files
                last_write_time = current_second
        except Exception as e:
            log("Error: " + str(e))
            log(traceback.format_exc())
            sleep(5)  # Prevent crash loop