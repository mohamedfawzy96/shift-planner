import numpy as np


class DriverSchedule:
    driver_id_index = 0
    weights_values = {
        "routes": -100,
        "forced_days": -100
    }
    route_scores = []

    def __init__(self, forced_days_file: str = '../data/forced_day_off.csv',
                 qualified_route_file: str = '../data/qualified_route.csv',
                 number_of_days: int = 14,
                 number_of_routes: int = 3):
        self.forced_days_off_raw_data = np.genfromtxt(forced_days_file, delimiter=',', skip_header=True)
        self.forced_days_off_matrix = self.forced_days_off_raw_data[:, 1:]
        self.drivers_ids = self.forced_days_off_raw_data[:, 0]
        self.qualified_route_matrix = np.genfromtxt(qualified_route_file, delimiter=',', skip_header=True)[:, 1:]
        self.days_scores = self.forced_days_off_matrix * 0

        self.number_of_days = number_of_days
        self.number_of_routes = number_of_routes
        self.compute_scores_without_routes()
        self.compute_route_scores()

    def compute_scores_without_routes(self):
        self.days_scores = self.days_scores + (self.forced_days_off_matrix * self.weights_values["forced_days"])

    def get_scores_for_route(self, route_number: int):
        # i starts from 1 to skip driver id
        route_col = self.qualified_route_matrix[:, route_number]
        route_col = route_col == 0
        route_col = route_col
        route_col = route_col.reshape(route_col.shape[0], 1)
        route_score_matrix = self.days_scores + (route_col * self.weights_values["routes"])
        return route_score_matrix

    def get_drivers_for_route_sorted(self, day, route):
        score_route = self.route_scores[route]
        day_scores = score_route[:, day]
        indexes = day_scores.argsort(kind="mergesort")
        return self.drivers_ids[indexes]

    def compute_route_scores(self):
        for i in range(self.number_of_routes):
            route_score = self.get_scores_for_route(i)
            self.route_scores.append(route_score)

    def get_routes_sorted_by_available_drivers(self, day):
        day_scores = np.array([])
        for i in range(self.number_of_routes):
            route_score = self.route_scores[i]
            day_score = route_score[:, day]
            day_score = day_score >= 0
            day_score = np.sum(day_score)
            day_scores = np.append(day_scores, day_score)
        return day_scores.argsort(kind="mergesort"), day_scores

driver_schedule = DriverSchedule()
print(driver_schedule.get_routes_sorted_by_available_drivers(1))

# TODO: make sure to take from the array with la rgest number
routes = []
csv_data = []
for day in range(14):
    drives_used = {}
    routes_indexes, available_driver_counts = driver_schedule.get_routes_sorted_by_available_drivers(day)
    for routes_index in routes_indexes:
        availabe_drivers_cnt = int(available_driver_counts[routes_index])
        drivers_available = driver_schedule.get_drivers_for_route_sorted(day, routes_index)[-availabe_drivers_cnt:]
        shift_counter = 1
        driver_counter = 1
        while shift_counter < 3 and driver_counter <= availabe_drivers_cnt:
            driver_id = drivers_available[-driver_counter]
            driver_counter += 1
            if drives_used.get(driver_id, None) is not None:
                continue
            shift_counter += 1
            drives_used[driver_id] = True
            score_route = driver_schedule.route_scores[routes_index]
            day_scores = score_route[:, day]
            day_scores = day_scores.reshape(day_scores.shape[0], 1)
            driver_index= int(driver_id-1)
            print(day_scores[driver_index][0])
            if day_scores[driver_index][0] < 0:
                raise Exception("issue with negatives")
            csv_data.append(
                [driver_id, "day" + str(day+1), "route" + str(routes_index+1), "shift" + str(shift_counter-1)])

print(np.array(csv_data))
np.array(csv_data).tofile("foo.csv", sep=",")
