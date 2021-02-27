import numpy as np


class Schedule:

    def __init__(self, cols: int = 4):
        self.schedule_arr = np.empty((0, 4))

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
        return row

    def get_schedule(self) -> np.array:
        return self.schedule_arr

    def get_days_columns(self):
        return self.get_schedule()[:, 1]

    def get_drivers_columns(self):
        return self.get_schedule()[:, 0]