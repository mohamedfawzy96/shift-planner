import pytest
import numpy as np

from app.models import Schedule
from app.services import ScheduleService, TableService

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
    drivers = schedule.get_day_drivers(day_index)
    assert len(drivers) == len(np.unique(drivers))


@pytest.mark.parametrize("day_index", [i for i in range(schedule_service.get_no_days())])
def test_forced_days_off(day_index):
    """Test every shift for every route of the day has unique driver"""
    forced_day_ser = TableService('forced_day_off.csv')
    day_drivers = schedule.get_day_drivers(day_index)
    off_drivers = forced_day_ser.get_drivers_for_index(day_index)
    sub = list(set(day_drivers) - set(off_drivers))
    assert len(day_drivers) == len(sub)


@pytest.mark.parametrize("route_index", [i for i in range(schedule_service.get_no_routes())])
def test_route_off(route_index):
    """Test every shift for every route of the day has unique driver"""
    route_driver_ser = TableService('qualified_route.csv')
    route_drivers = schedule.get_route_drivers(route_index)
    qual_route_drivers = route_driver_ser.get_drivers_for_index(route_index)
    sub = list(set(route_drivers) - set(qual_route_drivers))
    assert len(sub) == 0
