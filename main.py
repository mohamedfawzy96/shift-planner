from app.services import ScheduleService, TableService
import numpy as np

schedule_service = ScheduleService()
schedule_service.update_driver_used_score(1)
indexes, driver = schedule_service.get_available_drivers_for_route(1, 1)

schedule = schedule_service.create_schedule()
print(schedule_service.drivers_scores)
print(schedule.get_schedule())
ditc_dri = schedule.get_drivers_dict()
c = 0
for driver in ditc_dri:
    if "shift2" in ditc_dri[driver]["shifts"] and ditc_dri[driver]["shifts"]["shift2"] > 4:
        print(driver, ditc_dri[driver]["shifts"]["shift2"] )
        c += 1
print("############ " + str(c))
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
