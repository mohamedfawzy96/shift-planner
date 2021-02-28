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

    def get_schedule_array(self) -> np.array:
        return self.schedule_arr

    def get_days_columns(self):
        return self.get_schedule_array()[:, 1]

    def get_drivers_columns(self):
        return self.get_schedule_array()[:, 0]

    def get_day_drivers(self, day_index: int):
        formated_day = Schedule.format_day(day_index)
        return self.get_day_dict()[formated_day]["drivers"]

    def get_route_drivers(self, route_index: int):
        formated_route = Schedule.format_route(route_index)
        return self.get_routes_dict()[formated_route]["drivers"]

    def is_driver_used(self, day_index: int, shift_index: int, driver_id: int):
        return self.is_driver_day_used(day_index, driver_id) or self.is_driver_shift_used(shift_index, driver_id)

    def get_day_dict(self):
        return self.schedule_dict["days"]

    def get_routes_dict(self):
        return self.schedule_dict["routes"]

    def get_drivers_dict(self):
        return self.schedule_dict["drivers"]

    def is_driver_day_used(self, day_index: int, driver_id: int):
        """
        Checks if the driver has been used on this day using the scheduler dict
        :param day_index: int
        :param driver_id: int
        :return: bool
        """
        drivers_dict = self.get_drivers_dict()
        driver_format = self.format_driver(driver_id)
        day_format = self.format_day(day_index)
        driver_dict_days = drivers_dict.get(driver_format, {}).get("days", {})
        driver_used = driver_dict_days.get(day_format, False)
        return driver_used

    def is_driver_shift_used(self, shift_index: int, driver_id: int) -> bool:
        """
        Checks if driver has been assigned to more than 4 shifts
        :param shift_index: int
        :param driver_id: int
        :return: bool
        """
        drivers_dict = self.get_drivers_dict()
        driver_format = self.format_driver(driver_id)
        shift_format = self.format_shift(shift_index)
        driver_dict_shifts = drivers_dict.get(driver_format, {}).get("shifts", {})
        driver_used = driver_dict_shifts.get(shift_format, 0) >= 4
        return driver_used

    def add_row(self, driver_id: int, day_index: int, routes_index: int, shift_index: int) -> list:
        """
        Adds to row to schedule and updates the schedule dict
        :param driver_id: int
        :param day_index: int
        :param routes_index: int
        :param shift_index: int
        :return: list
        """
        row = [driver_id,
               Schedule.format_day(day_index),
               Schedule.format_route(routes_index),
               Schedule.format_shift(shift_index)]
        self.schedule_arr = np.append(self.schedule_arr, np.array([row]), axis=0)
        self.__add_to_dict(driver_id, day_index, routes_index, shift_index)

        return row

    def __add_to_dict(self, driver_id: int, day_index: int, routes_index: int, shift_index: int):
        """
        Performs dict update operations for driver, day and route
        :param driver_id: int
        :param day_index: int
        :param routes_index: int
        :param shift_index: int
        """
        day_formatted = Schedule.format_day(day_index)
        self.__add_driver_arr_to_dict(day_formatted, driver_id, self.get_day_dict())

        route_formatted = Schedule.format_route(routes_index)
        self.__add_driver_arr_to_dict(route_formatted, driver_id, self.get_routes_dict())

        shift_formatted = Schedule.format_shift(shift_index)

        self.__add_driver_info_to_dict(driver_id, day_formatted, shift_formatted)

    def __add_driver_info_to_dict(self, driver_id: int, day_formatted: str, shift_formated: str):
        """
        :param driver_id: int
        :param day_formatted: str
        :param shift_formated: str
        :return:
        """
        drivers_dict = self.get_drivers_dict()
        driver_formated = Schedule.format_driver(driver_id)
        driver = drivers_dict.get(driver_formated, {})
        driver["days"] = driver.get("days", {})
        driver["days"][day_formatted] = True

        driver_shifts = driver.get("shifts", {})
        driver_shifts[shift_formated] = driver_shifts.get(shift_formated, 0) + 1
        driver["shifts"] = driver_shifts
        drivers_dict[driver_formated] = driver

    def __add_driver_arr_to_dict(self, formated_col: str, driver_id: int, parent_dict: dict):
        """
        adds new driver to drivers array of the  parent_dict
        :param formated_col:str
        :param driver_id: int
        :param parent_dict: dict
        :return: parent_dict : dict
        """
        ob_dict = parent_dict.get(formated_col, {})
        ob_dict = self.__add_key_to_dict_arr(ob_dict, driver_id, "drivers")
        parent_dict[formated_col] = ob_dict
        return parent_dict

    def __add_key_to_dict_arr(self, ob_dict, value, key):
        drivers = ob_dict.get(key, [])
        drivers.append(value)
        ob_dict[key] = drivers
        return ob_dict
