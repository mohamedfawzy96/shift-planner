from app.services import ScheduleService, TableService
import numpy as np

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
print(schedule.get_schedule())

route_driver_ser = TableService('qualified_route.csv')
route_drivers = schedule.get_route_drivers(0)
qual_route_drivers = route_driver_ser.get_drivers_for_index(0)
sub = list(set(route_drivers) - set(qual_route_drivers))

print(set(route_drivers) - set(qual_route_drivers))
print(qual_route_drivers)

