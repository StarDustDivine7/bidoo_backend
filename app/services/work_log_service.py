from datetime import date

from app.model.work_log import WorkLog
from app.repository.work_log_repository import WorkLogRepository
from app.schemas.work_log_schemas import WorkLogCreate


class WorkLogService:
    """Daily work update business rules yaha rakhe gaye hain."""

    def __init__(self, work_log_repository: WorkLogRepository):
        self.work_log_repository = work_log_repository

    def create_work_log(self, user_id: int, payload: WorkLogCreate) -> WorkLog:
        work_date = payload.work_date or date.today()
        work_log = WorkLog(
            user_id=user_id,
            work_date=work_date,
            summary=payload.summary,
            blockers=payload.blockers,
            hours_spent=payload.hours_spent,
        )
        return self.work_log_repository.create(work_log)

    def list_user_work_logs(self, user_id: int) -> list[WorkLog]:
        return self.work_log_repository.get_for_user(user_id)
