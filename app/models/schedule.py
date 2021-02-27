import numpy as np


class Schedule:

    def __init__(self, cols: int = 4):
        self.schedule_arr = np.empty((0, 4))
        self.schedule_dict = {}

    @staticmethod
    def format_day(day_index: int) -> str:
        return "day" + str(day_index + 1)

    @staticmethod
    def format_shift(shift_index: int) -> str:
        return "shift" + str(shift_index + 1)

    @staticmethod
    def format_route(route_index: int) -> str:
        return "route" + str(route_index + 1)

    def add_row(self, driver_id: int, day_index: int, routes_index: int, shift_index: int) -> list:
        row = [driver_id,
               Schedule.format_day(day_index),
               Schedule.format_route(routes_index),
               Schedule.format_shift(shift_index)]
        self.schedule_arr = np.append(self.schedule_arr, np.array([row]), axis=0)
        self.add_to_dict(driver_id, day_index, routes_index, shift_index)

        return row

    def add_to_dict(self, driver_id: int, day_index: int, routes_index: int, shift_index: int):
        day_formated_col = Schedule.format_day(day_index)
        self.__add_driver_to_dict(day_formated_col, driver_id)

        route_formated_col = Schedule.format_route(routes_index)
        self.__add_driver_to_dict(route_formated_col, driver_id)

    def __add_driver_to_dict(self, formated_col, driver_id):
        ob_dict = self.schedule_dict.get(formated_col, {})
        ob_dict = self.__add_drivers_to_dict_helper(ob_dict, driver_id)
        self.schedule_dict[formated_col] = ob_dict

    def __add_drivers_to_dict_helper(self, ob_dict, driver_id):
        drivers = ob_dict.get("drivers", [])
        drivers.append(driver_id)
        ob_dict["drivers"] = drivers
        return ob_dict

    def get_schedule(self) -> np.array:
        return self.schedule_arr

    def get_days_columns(self):
        return self.get_schedule()[:, 1]

    def get_drivers_columns(self):
        return self.get_schedule()[:, 0]

    def get_day_drivers(self, day_index):
        formated_day = Schedule.format_day(day_index)
        return self.schedule_dict[formated_day]["drivers"]

    def get_route_drivers(self, route_index):
        formated_route = Schedule.format_route(route_index)
        return self.schedule_dict[formated_route]["drivers"]
