from app.models import Schedule
from app.services import ScheduleService, TableService
import numpy as np
import time as t

BASE_DIR = "./data/case1/"

use_default = input("Do you want to use the default directory (./data/case1/) for input files [y/n]: ")
if use_default == "n":
    print("Please provide directory that contains input files")
    print("Don't forget to add the / at the end of the directory:")
    BASE_DIR = input("Your directory: ")

schedule_service = ScheduleService(
    forced_days_file=BASE_DIR + 'forced_day_off.csv',
    qualified_route_file=BASE_DIR + 'qualified_route.csv',
    pref_days_file=BASE_DIR + 'pref_day_off.csv',
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
