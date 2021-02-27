from app.services import ScheduleService, TableService
import numpy as np

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
print(schedule.get_schedule())

forced_day_ser = TableService('forced_day_off.csv')
day_drivers = schedule.get_day_drivers(0)
off_drivers = forced_day_ser.get_drivers_for_index(0)
print(day_drivers)
print(off_drivers)

print(set(day_drivers) - set(off_drivers))

