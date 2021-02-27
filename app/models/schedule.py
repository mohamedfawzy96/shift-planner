import numpy as np


class Schedule:

    def __init__(self, cols: int = 4):
        self.schedule_arr = np.empty((0, 4))
        self.schedule_dict = {
            "days": {},
            "routes": {},
            "drivers": {}
        }

    @staticmethod
    def format_day(day_index: int) -> str:
        return "day" + str(day_index + 1)

    @staticmethod
    def format_shift(shift_index: int) -> str:
        return "shift" + str(shift_index + 1)

    @staticmethod
    def format_route(route_index: int) -> str:
        return "route" + str(route_index + 1)

    @staticmethod
    def format_driver(driver_id: int) -> str:
        return "driver" + str(driver_id)

    def get_schedule(self) -> np.array:
        return self.schedule_arr

    def get_days_columns(self):
        return self.get_schedule()[:, 1]

    def get_drivers_columns(self):
        return self.get_schedule()[:, 0]

    def get_day_drivers(self, day_index: int):
        formated_day = Schedule.format_day(day_index)
        return self.get_day_dict()[formated_day]["drivers"]

    def get_route_drivers(self, route_index: int):
        formated_route = Schedule.format_route(route_index)
        return self.get_routes_dict()[formated_route]["drivers"]

    def is_driver_used(self, day: int, driver_id: int):
        drivers_dict = self.get_drivers_dict()
        driver_format = self.format_driver(driver_id)
        day_format = self.format_day(day)

        driver_dict = drivers_dict.get(driver_format, {})
        driver_used = driver_dict.get(day_format, False)

        return driver_used

    def get_day_dict(self):
        return self.schedule_dict["days"]

    def get_routes_dict(self):
        return self.schedule_dict["routes"]

    def get_drivers_dict(self):
        return self.schedule_dict["drivers"]

    def add_row(self, driver_id: int, day_index: int, routes_index: int, shift_index: int) -> list:
        row = [driver_id,
               Schedule.format_day(day_index),
               Schedule.format_route(routes_index),
               Schedule.format_shift(shift_index)]
        self.schedule_arr = np.append(self.schedule_arr, np.array([row]), axis=0)
        self.__add_to_dict(driver_id, day_index, routes_index, shift_index)

        return row

    def __add_to_dict(self, driver_id: int, day_index: int, routes_index: int, shift_index: int):
        day_formatted = Schedule.format_day(day_index)
        self.__add_driver_arr_to_dict(day_formatted, driver_id, self.get_day_dict())

        route_formatted = Schedule.format_route(routes_index)
        self.__add_driver_arr_to_dict(route_formatted, driver_id, self.get_routes_dict())

        shift_formatted = Schedule.format_shift(shift_index)

        self.__add_driver_info_to_dict(driver_id, day_formatted, shift_formatted)

    def __add_driver_info_to_dict(self, driver_id: int, day_formatted: str, shift_formated: str):
        drivers_dict = self.get_drivers_dict()
        driver_formated = Schedule.format_driver(driver_id)
        driver = drivers_dict.get(driver_formated, {})
        driver[day_formatted] = True
        drivers_dict[driver_formated] = driver

    def __add_driver_arr_to_dict(self, formated_col: str, driver_id: int, parent_dict: dict):
        ob_dict = parent_dict.get(formated_col, {})
        ob_dict = self.__add_key_to_dict_arr(ob_dict, driver_id, "drivers")
        parent_dict[formated_col] = ob_dict
        return parent_dict

    def __add_key_to_dict_arr(self, ob_dict, value, key):
        drivers = ob_dict.get(key, [])
        drivers.append(value)
        ob_dict[key] = drivers
        return ob_dict
