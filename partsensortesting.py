from pms5003 import PMS5003

pms5003 = PMS5003()

part_mat_readings_raw = pms5003.read()
part_mat_readings = str(part_mat_readings_raw).strip()

print(part_mat_readings)