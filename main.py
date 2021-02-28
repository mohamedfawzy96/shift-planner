from app.models import Schedule
from app.services import ScheduleService, TableService
import numpy as np
import time as t


# just for testing
def add_warning(schedule_obj: Schedule):
    ditc_dri = schedule_obj.get_drivers_dict()
    c = 0
    for driver in ditc_dri:
        if "shift2" in ditc_dri[driver]["shifts"] and ditc_dri[driver]["shifts"]["shift2"] > 4:
            c += 1
    if c > 0:
        print("######## WARNING ###########")
        print(str(c), " Drivers have more than 4 night shifts")
        print("#############################")
        print("\n")


CASE_DIR = "case1"

schedule_service = ScheduleService(
    forced_days_file=CASE_DIR + '/forced_day_off.csv',
    qualified_route_file=CASE_DIR + '/qualified_route.csv',
    pref_days_file=CASE_DIR + '/pref_day_off.csv',
)

schedule = schedule_service.create_schedule()
add_warning(schedule)

OUTPUT_BASE_DIR = "./data/output/"

time = t.time()
file = OUTPUT_BASE_DIR + str(int(time)) + "_schedule.csv"
np.savetxt(file, schedule.get_schedule_array(), delimiter=',', fmt='%s')
print("########################################")
print("\n")
print("Please find schedule in this file: " + file)
print("\n")
print("########################################")
