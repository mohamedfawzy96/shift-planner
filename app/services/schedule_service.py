import numpy as np
import time
from app.models import Schedule
from .table_service import TableService


class ScheduleService:
    driver_id_index = 0
    weights_values = {
        "unqualified_routes": -100,
        "forced_days": -100,
        "pref_working_days": -0.5,
        "driver_used": -0.5
    }
    route_days_scores = []
    min_available_score = 0
    init_score = 20
    night_shift_index = 1

    def __init__(self, forced_days_file: str = 'case1/forced_day_off.csv',
                 qualified_route_file: str = 'case1/qualified_route.csv',
                 pref_days_file: str = 'case1/pref_day_off.csv',
                 number_of_days: int = 14,
                 number_of_routes: int = 3,
                 number_of_shifts: int = 2):

        self.qual_route_ser = TableService(qualified_route_file)
        self.forced_days_ser = TableService(forced_days_file)
        self.perfer_days_ser = TableService(pref_days_file)

        self.drivers_ids = self.forced_days_ser.get_drivers()

        self.days_scores = np.zeros(self.forced_days_ser.get_matrix().shape) + self.init_score
        self.drivers_scores = np.zeros(self.forced_days_ser.get_matrix().shape)
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

    def get_driver_id_by_index(self, driver_index: int):
        return self.drivers_ids[driver_index]

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

        route_score_matrix = self.days_scores + (invert_route_col * self.weights_values["unqualified_routes"])
        return route_score_matrix

    def get_available_drivers_for_route(self, day: int, route: int) -> np.array:
        """
        :param day: int
        :param route: int
        :return: (array, int) array of available drivers indexes sorted ASC by their score for this day's route, count of drivers (int)
        """
        score_route = self.route_days_scores[route] + self.drivers_scores
        day_scores = score_route[:, day]
        indexes = day_scores.argsort(kind="mergesort")

        driv_cnt = np.sum(day_scores >= self.min_available_score)

        return indexes[-driv_cnt:], driv_cnt

    def __compute_route_scores(self):
        """
        Computes scores for each route, each cell in the score matrix corresponds
        to the score from  the driver for a specific day
        """
        for i in range(self.get_no_routes()):
            route_day_score = self.__get_scores_for_days_route(i)
            self.route_days_scores.append(route_day_score)

    def update_driver_used_score(self, driver_index: int):
        self.drivers_scores[driver_index, :] = self.drivers_scores[driver_index, :] + self.weights_values["driver_used"]

    def __get_routes_srt_by_dri_cnt(self, day: int):
        """
        :param day: int
        :return: (array of the route indexes sorted ASC by drivers cnt,
                  array of available drivers for each route)
        """
        driv_cnts = np.array([])
        routes_drivers_indexes = []

        for i in range(self.get_no_routes()):
            available_drivers_indexes, driv_cnt = self.get_available_drivers_for_route(day, i)
            driv_cnts = np.append(driv_cnts, driv_cnt)
            routes_drivers_indexes.append(available_drivers_indexes)
        route_indexes = driv_cnts.argsort(kind="mergesort")
        return route_indexes, routes_drivers_indexes

    def create_schedule(self) -> Schedule:
        """
        :return: returns a Schedule object that has all information about the schedule
        """
        schedule = Schedule()
        for day_index in range(self.get_no_days()):

            """ 
                NOTE: routes_indexes_sorted  consist of indices and not the actual values, the first
                element for example is the index of the route with the lowest number of drivers available   
            """
            routes_indexes_sorted, available_drivers_indexes = self.__get_routes_srt_by_dri_cnt(day_index)
            for routes_index in routes_indexes_sorted:
                """ 
                    NOTE: drivers_indexes_sorted  consist of indices and not the actual values, the first
                    element for example is the index of the driver with the lowest score  
                """
                drivers_indexes_sorted = available_drivers_indexes[routes_index]
                shift_index, driver_counter = self.get_no_shifts() - 1, 1
                number_of_drivers = len(drivers_indexes_sorted)

                """
                assigning drivers to the night shift first is important
                because drivers are sorted with their scores and this score
                is based on different things one of them is the number of night
                shifts this driver has been assigned to, so giving the night shift
                drivers with high scores is important 
                """
                while shift_index >= 0 and driver_counter <= number_of_drivers:
                    driver_index = drivers_indexes_sorted[-driver_counter]
                    driver_id = self.get_driver_id_by_index(driver_index)
                    driver_counter += 1

                    if schedule.is_driver_day_used(day_index, driver_id):
                        continue
                    schedule.add_row(driver_id, day_index, routes_index, shift_index)

                    if shift_index == self.night_shift_index:
                        self.update_driver_used_score(driver_index)
                    shift_index -= 1

        return schedule
