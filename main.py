from app.services import ScheduleService, TableService
import numpy as np

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
print(schedule.get_schedule())
# print(schedule.get_drivers_dict())
#
# route_driver_ser = TableService('qualified_route.csv')
# route_drivers = schedule.get_day_drivers(13)
# qual_route_drivers = route_driver_ser.get_drivers_for_index(0)
# print(route_drivers)
# sub = list(set(route_drivers) - set(qual_route_drivers))
#
# print(set(route_drivers) - set(qual_route_drivers))
# print(qual_route_drivers)

