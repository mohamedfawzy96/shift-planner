from app.services import ScheduleService, TableService
import numpy as np

schedule_service = ScheduleService(
    forced_days_file='case2/forced_day_off.csv',
    qualified_route_file='case2/qualified_route.csv',
    pref_days_file='case2/pref_day_off.csv',
)
schedule = schedule_service.create_schedule()

# self.raw_data = np.genfromtxt(self.base_dir + file, delimiter=',', skip_header=True)
# start_id = self.raw_data.shape[0] + 1
# for row in self.raw_data:
#     new_row = row
#     new_row[0] = start_id
#     np.append(self.raw_data, np.array([row]), axis=0)
#     start_id += 1
# schedule_service.update_driver_used_score(1)
# indexes, driver = schedule_service.get_available_drivers_for_route(1, 1)

# schedule = schedule_service.create_schedule()
print(schedule.get_schedule())
ditc_dri = schedule.get_drivers_dict()
c = 0
for driver in ditc_dri:
    if "shift2" in ditc_dri[driver]["shifts"] and ditc_dri[driver]["shifts"]["shift2"] > 4:
        print(driver, ditc_dri[driver]["shifts"]["shift2"])
        c += 1
print("############ " + str(c))
#
# route_driver_ser = TableService('qualified_route.csv')
# route_drivers = schedule.get_day_drivers(13)
# qual_route_drivers = route_driver_ser.get_drivers_for_index(0)
# print(route_drivers)
# sub = list(set(route_drivers) - set(qual_route_drivers))
#
# print(set(route_drivers) - set(qual_route_drivers))
# print(qual_route_drivers)
