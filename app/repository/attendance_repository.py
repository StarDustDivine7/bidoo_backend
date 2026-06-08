from datetime import date

from sqlalchemy.orm import Session

from app.model.attendance import Attendance


class AttendanceRepository:
    """Attendance records ko read/write karne ke liye helper."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_user_and_date(self, user_id: int, attendance_date: date) -> Attendance | None:
        return (
            self.db.query(Attendance)
            .filter(Attendance.user_id == user_id, Attendance.attendance_date == attendance_date)
            .first()
        )

    def create(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def save(self, attendance: Attendance) -> Attendance:
        self.db.add(attendance)
        self.db.commit()
        self.db.refresh(attendance)
        return attendance

    def count_marked_for_date(self, attendance_date: date) -> int:
        return self.db.query(Attendance).filter(Attendance.attendance_date == attendance_date).count()
