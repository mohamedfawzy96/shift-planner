import pytest
import numpy as np

from app.models import Schedule
from app.services import ScheduleService

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
np_schedule = schedule.get_schedule()


@pytest.mark.parametrize("day_index", [i for i in range(schedule_service.get_no_days())])
def test_all_shifts_assigned(day_index):
    """Test every shift of the day for each route is assigned"""
    days_col = schedule.get_days_columns()
    is_day = days_col == Schedule.format_day(day_index)
    number_of_shifts = np.sum(is_day)

    no_routes = schedule_service.get_no_routes()
    no_shifts = schedule_service.get_no_shifts()

    assert number_of_shifts == no_routes * no_shifts


@pytest.mark.parametrize("day_index", [i for i in range(schedule_service.get_no_days())])
def test_unique_drivers_in_day(day_index):
    """Test every shift for every route of the day has unique driver"""
    days_col = schedule.get_days_columns()
    day_indexes = np.argwhere(days_col == schedule.format_day(day_index))

    drivers_col = schedule.get_drivers_columns()
    drivers = drivers_col[day_indexes]
    assert len(drivers) == len(np.unique(drivers))

