import numpy as np
import time
from app.models import Schedule
from .table_service import TableService


class ScheduleService:
    driver_id_index = 0
    weights_values = {
        "routes": -20,
        "forced_days": -20,
        "pref_working_days": -1
    }
    route_days_scores = []
    min_available_score = 0
    init_score = 10

    def __init__(self, forced_days_file: str = 'forced_day_off.csv',
                 qualified_route_file: str = 'qualified_route.csv',
                 pref_days_file: str = 'pref_day_off.csv',
                 number_of_days: int = 14,
                 number_of_routes: int = 3,
                 number_of_shifts: int = 2):

        self.qual_route_ser = TableService(qualified_route_file)
        self.forced_days_ser = TableService(forced_days_file)
        self.perfer_days_ser = TableService(pref_days_file)

        self.drivers_ids = self.forced_days_ser.get_drivers()

        self.days_scores = np.zeros(self.forced_days_ser.get_matrix().shape) + self.init_score

        self.number_of_days = number_of_days
        self.number_of_routes = number_of_routes
        self.number_of_shifts = number_of_shifts

        self.__compute_scores_without_routes()
        self.__compute_route_scores()

    def get_no_days(self) -> int:
        return self.number_of_days

    def get_no_shifts(self) -> int:
        return self.number_of_shifts

    def get_no_routes(self) -> int:
        return self.number_of_routes

    def __compute_scores_without_routes(self):
        def compute_forc_day_off_scr():
            forced_matrix = self.forced_days_ser.get_matrix()
            self.days_scores = self.days_scores + (forced_matrix * self.weights_values["forced_days"])

        def compute_pref_day_off_scr():
            invert_pref_day = self.perfer_days_ser.get_matrix() == 0
            self.days_scores = self.days_scores + (invert_pref_day * self.weights_values["pref_working_days"])

        score_funcs = [compute_forc_day_off_scr, compute_pref_day_off_scr]
        for score_func in score_funcs:
            score_func()

    def __get_scores_for_days_route(self, route_index: int) -> np.array:
        """
        :param route_index: route index
        :return: matrix of computed score for each day and driver depending on the route
        """

        route_col = self.qual_route_ser.get_col_by_index(route_index)
        invert_route_col = route_col == 0
        invert_route_col = invert_route_col.reshape(route_col.shape[0], 1)

        route_score_matrix = self.days_scores + (invert_route_col * self.weights_values["routes"])
        return route_score_matrix

    def __get_available_drivers_for_route(self, day: int, route: int) -> np.array:
        """
        :param day: index of day
        :param route: index of route
        :return: array of available driver ids sorted ASC by their score for this day route
        """
        score_route = self.route_days_scores[route]
        day_scores = score_route[:, day]
        indexes = day_scores.argsort(kind="mergesort")
        return self.drivers_ids[indexes]

    def __compute_route_scores(self):
        """
        Computes scores for each route, each cell in the score matrix corresponds
        to the score from  the driver for a specific day
        """
        for i in range(self.get_no_routes()):
            route_day_score = self.__get_scores_for_days_route(i)
            self.route_days_scores.append(route_day_score)
        print(self.route_days_scores[0])


    def __get_routes_srt_by_dri_cnt(self, day: int):
        """
        :param day: index of day
        :return: (array of the route indexes sorted ASC by drivers cnt,
                  array of available drivers for each route)
        """
        driv_cnts = np.array([])
        drivers_cnt_for_routes = []

        for i in range(self.get_no_routes()):
            route_score = self.route_days_scores[i]
            day_score = route_score[:, day]

            driv_cnt = np.sum(day_score >= self.min_available_score)
            driv_cnts = np.append(driv_cnts, driv_cnt)

            # removing drivers with score below min required score
            available_drivers = self.__get_available_drivers_for_route(day, i)[-driv_cnt:]

            drivers_cnt_for_routes.append(available_drivers)

        return driv_cnts.argsort(kind="mergesort"), drivers_cnt_for_routes

    def create_schedule(self) -> Schedule:
        """
        :return: returns a Schedule object that has all information about the schedule
        """
        schedule = Schedule()
        for day_index in range(self.get_no_days()):
            routes_indexes_sorted, available_drivers_routes = self.__get_routes_srt_by_dri_cnt(day_index)
            for routes_index in routes_indexes_sorted:
                route_drivers_sorted = available_drivers_routes[routes_index]
                shift_index, driver_counter = 0, 1
                number_of_drivers = len(route_drivers_sorted)
                while shift_index < self.get_no_shifts() and driver_counter <= number_of_drivers:
                    driver_id = route_drivers_sorted[-driver_counter]
                    driver_counter += 1
                    if schedule.is_driver_day_used(day_index, driver_id):
                        continue
                    self.test(routes_index, driver_id, day_index)
                    schedule.add_row(driver_id, day_index, routes_index, shift_index)
                    shift_index += 1

        return schedule

    def test(self, routes_index, driver_id, day):
        score_route = self.route_days_scores[routes_index]
        day_scores = score_route[:, day]
        day_scores = day_scores.reshape(day_scores.shape[0], 1)
        driver_index = int(driver_id - 1)
        if day_scores[driver_index][0] < 0:
            raise Exception("issue with negatives")
