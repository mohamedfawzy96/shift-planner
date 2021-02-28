import pytest
import numpy as np

from app.models import Schedule
from app.services import ScheduleService, TableService


def get_cases():
    case_tests = []
    cases = ["case1", "case2", "case3"]
    for i in range(len(cases)):
        case = cases[i]
        schedule_service = ScheduleService(forced_days_file=case + '/forced_day_off.csv',
                                           qualified_route_file=case + '/qualified_route.csv',
                                           pref_days_file=case + '/pref_day_off.csv', )
        schedule = schedule_service.create_schedule()
        case_tests.append((schedule_service, schedule))
    return case_tests


case_tests = get_cases()


@pytest.mark.parametrize("schedule_service,schedule", case_tests)
def test_all_shifts_assigned(schedule_service, schedule):
    """Test every shift of the day for each route is assigned"""
    for day_index in range(schedule_service.get_no_days()):
        days_col = schedule.get_days_columns()
        is_day = days_col == Schedule.format_day(day_index)
        number_of_shifts = np.sum(is_day)

        no_routes = schedule_service.get_no_routes()
        no_shifts = schedule_service.get_no_shifts()

        assert number_of_shifts == no_routes * no_shifts


@pytest.mark.parametrize("schedule_service,schedule", case_tests)
def test_unique_drivers_in_day(schedule_service, schedule):
    """Test every shift for every route of the day has unique driver"""
    for day_index in range(schedule_service.get_no_days()):
        drivers = schedule.get_day_drivers(day_index)
        assert len(drivers) == len(np.unique(drivers))


@pytest.mark.parametrize("schedule_service,schedule", case_tests)
def test_forced_days_off(schedule_service, schedule):
    """Test every shift for every route of the day has unique driver"""
    for day_index in range(schedule_service.get_no_days()):
        forced_day_ser = schedule_service.forced_days_ser
        day_drivers = schedule.get_day_drivers(day_index)
        off_drivers = forced_day_ser.get_drivers_for_index(day_index)
        sub = list(set(day_drivers) - set(off_drivers))
        assert len(day_drivers) == len(sub)


@pytest.mark.parametrize("schedule_service,schedule", case_tests)
def test_route_off(schedule_service, schedule):
    """Test every shift for every route of the day has unique driver"""
    for route_index in range(schedule_service.get_no_routes()):
        route_driver_ser = schedule_service.qual_route_ser
        route_drivers = schedule.get_route_drivers(route_index)
        qual_route_drivers = route_driver_ser.get_drivers_for_index(route_index)
        sub = list(set(route_drivers) - set(qual_route_drivers))
        assert len(sub) == 0
