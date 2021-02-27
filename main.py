from app.services import ScheduleService

schedule_service = ScheduleService()
schedule = schedule_service.create_schedule()
print(schedule.get_schedule_as_np())
