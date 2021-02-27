import pytest
import numpy as np

from app.services import ScheduleService, Schedule

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
np_schedule = schedule.get_schedule_as_np()


@pytest.mark.parametrize("day_index", [i for i in range(schedule_service.get_no_days())])
def test_all_shifts_assigned(day_index):
    is_day = np_schedule[:, 1] == Schedule.format_day(day_index)
    number_of_shifts = np.sum(is_day)

    no_routes = schedule_service.get_no_routes()
    no_shifts = schedule_service.get_no_shifts()

    assert number_of_shifts == no_routes * no_shifts


# @pytest.mark.parametrize("day_index", [i for i in range(schedule_service.get_no_days())])
# def unique_drivers_in_day(day_index):
