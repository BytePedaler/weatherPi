from pms5003 import PMS5003

pms5003 = PMS5003()

# pmr01 = part_mat_readings.replace(" ", "")
# pmr02 = pmr01.strip('\n')

def pm_data_scraping():
    part_mat_readings_raw = pms5003.read()
    part_mat_readings = str(part_mat_readings_raw)
    pm_readings = []

    # Spliting data into lines
    msm_data_lines = part_mat_readings.split('\n')

    for line in msm_data_lines:
        parts = line.split(':')
        if len(parts) > 1:
            measurement = parts[1].strip()
            pm_readings.append(measurement)

    return(pm_readings)