from app.services import ScheduleService, TableService
import numpy as np
import time as t

CASE_DIR = "case3"

schedule_service = ScheduleService(
    forced_days_file=CASE_DIR + '/forced_day_off.csv',
    qualified_route_file=CASE_DIR + '/qualified_route.csv',
    pref_days_file=CASE_DIR + '/pref_day_off.csv',
)
schedule = schedule_service.create_schedule()
ditc_dri = schedule.get_drivers_dict()
c = 0
for driver in ditc_dri:
    if "shift2" in ditc_dri[driver]["shifts"] and ditc_dri[driver]["shifts"]["shift2"] > 4:
        print(driver, ditc_dri[driver]["shifts"]["shift2"] )
        print(driver, ditc_dri[driver]["shifts"]["shift2"])
        c += 1
print("############ " + str(c))

OUTPUT_BASE_DIR = "./data/output/"

time = t.time()
file = OUTPUT_BASE_DIR + str(int(time)) + "_schedule.csv"
np.savetxt(file, schedule.get_schedule_array(), delimiter=',', fmt='%s')
print("########################################")
print("\n")
print("Please find schedule in this file: " + file)
print("\n")
print("########################################")
