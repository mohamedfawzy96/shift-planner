from app.models import Schedule
from app.services import ScheduleService, TableService
import numpy as np
import time as t

CASE_DIR = "./data/case1/"

schedule_service = ScheduleService(
    forced_days_file=CASE_DIR + 'forced_day_off.csv',
    qualified_route_file=CASE_DIR + 'qualified_route.csv',
    pref_days_file=CASE_DIR + 'pref_day_off.csv',
)

schedule = schedule_service.create_schedule()

OUTPUT_BASE_DIR = "./data/output/"

time = t.time()
file = OUTPUT_BASE_DIR + str(int(time)) + "_schedule.csv"
np.savetxt(file, schedule.get_schedule_array(), delimiter=',', fmt='%s', header="driver,day,route,shift", comments='')
print("########################################")
print("\n")
print("Please find schedule in this file: " + file)
print("\n")
print("########################################")
