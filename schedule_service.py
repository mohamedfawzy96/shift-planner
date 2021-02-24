import numpy as np
import time


class ScoreService:
    driver_id_index = 0
    weights_values = {
        "routes": -10,
        "forced_days": -10,
        "pref_working_days": 1
    }
    route_scores = []

    def __init__(self, forced_days_file: str = '../data/forced_day_off.csv',
                 qualified_route_file: str = '../data/qualified_route.csv',
                 pref_days_file: str = '../data/pref_day_off.csv',
                 number_of_days: int = 14,
                 number_of_routes: int = 3):

        self.forced_days_off_raw_data = np.genfromtxt(forced_days_file, delimiter=',', skip_header=True)
        self.qualified_route_raw_data = np.genfromtxt(qualified_route_file, delimiter=',', skip_header=True)
        self.preferred_days_off_raw_data = np.genfromtxt(pref_days_file, delimiter=',', skip_header=True)

        self.qualified_route_matrix = self.qualified_route_raw_data[:, 1:]
        self.forced_days_off_matrix = self.forced_days_off_raw_data[:, 1:]
        self.preferred_days_off_matrix = self.preferred_days_off_raw_data[:, 1:]

        self.drivers_ids = self.forced_days_off_raw_data[:, 0]
        self.days_scores = self.forced_days_off_matrix * 0

        self.number_of_days = number_of_days
        self.number_of_routes = number_of_routes

        self.__compute_scores_without_routes()
        self.__compute_route_scores()

    def __compute_scores_without_routes(self):
        def compute_forc_day_off_scr():
            self.days_scores = self.days_scores + (self.forced_days_off_matrix * self.weights_values["forced_days"])

        def compute_pref_day_off_scr():
            invert_pref_day = self.preferred_days_off_matrix == 0
            self.days_scores = self.days_scores + (invert_pref_day * self.weights_values["pref_working_days"])

        score_funcs = [compute_forc_day_off_scr]
        for score_func in score_funcs:
            score_func()

    def get_scores_for_route(self, route_number: int):
        route_col = self.qualified_route_matrix[:, route_number]
        invert_route_col = route_col == 0
        invert_route_col = invert_route_col.reshape(route_col.shape[0], 1)
        route_score_matrix = self.days_scores + (invert_route_col * self.weights_values["routes"])
        return route_score_matrix

    def get_drivers_for_route_sorted(self, day: int, route: int):
        score_route = self.route_scores[route]
        day_scores = score_route[:, day]
        indexes = day_scores.argsort(kind="mergesort")
        return self.drivers_ids[indexes]

    def __compute_route_scores(self):
        for i in range(self.number_of_routes):
            route_score = self.get_scores_for_route(i)
            self.route_scores.append(route_score)

    def get_routes_srt_by_dri_cnt(self, day: int):
        day_scores = np.array([])
        drivers_for_routes = []
        for i in range(self.number_of_routes):
            route_score = self.route_scores[i]
            day_score = route_score[:, day]
            driv_cnt = np.sum(day_score >= 0)
            day_scores = np.append(day_scores, driv_cnt)
            available_drivers = self.get_drivers_for_route_sorted(day, i)[-driv_cnt:]
            drivers_for_routes.append(available_drivers)
        return day_scores.argsort(kind="mergesort"), drivers_for_routes

    def create_schedule(self):
        csv_data = []
        for day in range(self.number_of_days):
            drivers_used = {}
            routes_indexes_sorted, available_drivers_routes = self.get_routes_srt_by_dri_cnt(day)
            for routes_index in routes_indexes_sorted:
                route_drivers_sorted = available_drivers_routes[routes_index]
                shift_counter, driver_counter = 1, 1
                while shift_counter < 3 and driver_counter <= len(route_drivers_sorted):
                    driver_id = route_drivers_sorted[-driver_counter]
                    driver_counter += 1
                    if drivers_used.get(driver_id, None) is not None:
                        continue
                    drivers_used[driver_id] = True
                    self.test(routes_index, driver_id, day)
                    csv_data.append(
                        [driver_id, "day" + str(day + 1), "route" + str(routes_index + 1),
                         "shift" + str(shift_counter - 1)])
                    shift_counter += 1
        return np.array(csv_data)

    def test(self, routes_index, driver_id, day):
        score_route = self.route_scores[routes_index]
        day_scores = score_route[:, day]
        day_scores = day_scores.reshape(day_scores.shape[0], 1)
        driver_index = int(driver_id - 1)
        if day_scores[driver_index][0] < 0:
            raise Exception("issue with negatives")


driver_schedule = ScoreService()
driver_schedule.create_schedule()
# time1 = time.time()
# # TODO: make sure to take from the array with la rgest number
# routes = []
# csv_data = []
# for day in range(14):
#     drives_used = {}
#     routes_indexes, available_drivers_routes = driver_schedule.get_routes_srt_by_dri_cnt(day)
#     for routes_index in routes_indexes:
#         drivers_available = available_drivers_routes[routes_index]
#         shift_counter, driver_counter = 1, 1
#         while shift_counter < 3 and driver_counter <= len(drivers_available):
#             driver_id = drivers_available[-driver_counter]
#             driver_counter += 1
#             if drives_used.get(driver_id, None) is not None:
#                 continue
#             shift_counter += 1
#             drives_used[driver_id] = True
#             score_route = driver_schedule.route_scores[routes_index]
#             day_scores = score_route[:, day]
#             day_scores = day_scores.reshape(day_scores.shape[0], 1)
#             driver_index = int(driver_id - 1)
#             if day_scores[driver_index][0] < 0:
#                 raise Exception("issue with negatives")
#             csv_data.append(
#                 [driver_id, "day" + str(day + 1), "route" + str(routes_index + 1), "shift" + str(shift_counter - 1)])
#
# print(np.array(csv_data))
# np.array(csv_data).tofile("foo.csv", sep=",")
# print(time.time() - time1, " s")
