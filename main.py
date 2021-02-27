from app.services import ScheduleService
import numpy as np
schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
print(schedule.get_schedule())


days_col = schedule.get_days_columns()
day_indexes = np.argwhere(days_col == schedule.format_day(1))
drivers_col = schedule.get_drivers_columns()
drivers = drivers_col[day_indexes]