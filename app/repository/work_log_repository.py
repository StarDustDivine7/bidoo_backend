from datetime import date

from sqlalchemy.orm import Session

from app.model.work_log import WorkLog


class WorkLogRepository:
    """Daily work log queries ke liye repository layer."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, work_log: WorkLog) -> WorkLog:
        self.db.add(work_log)
        self.db.commit()
        self.db.refresh(work_log)
        return work_log

    def get_for_user(self, user_id: int) -> list[WorkLog]:
        return self.db.query(WorkLog).filter(WorkLog.user_id == user_id).order_by(WorkLog.work_date.desc()).all()

    def count_for_date(self, work_date: date) -> int:
        return self.db.query(WorkLog).filter(WorkLog.work_date == work_date).count()
