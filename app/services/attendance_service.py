from datetime import date, datetime

from fastapi import HTTPException, status

from app.model.attendance import Attendance
from app.repository.attendance_repository import AttendanceRepository


class AttendanceService:
    """Check-in, lunch aur check-out flow yaha handle hota hai."""

    def __init__(self, attendance_repository: AttendanceRepository):
        self.attendance_repository = attendance_repository

    def _get_or_create_today_record(self, user_id: int) -> Attendance:
        today = date.today()
        attendance = self.attendance_repository.get_by_user_and_date(user_id, today)
        if attendance:
            return attendance

        attendance = Attendance(user_id=user_id, attendance_date=today)
        return self.attendance_repository.create(attendance)

    def check_in(self, user_id: int) -> Attendance:
        attendance = self._get_or_create_today_record(user_id)
        if attendance.check_in_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aaj ka check-in already ho chuka hai")

        attendance.check_in_time = datetime.utcnow()
        return self.attendance_repository.save(attendance)

    def lunch_start(self, user_id: int) -> Attendance:
        attendance = self._get_or_create_today_record(user_id)
        if not attendance.check_in_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pehle check-in karna zaroori hai")
        if attendance.lunch_start_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lunch start already mark ho chuka hai")

        attendance.lunch_start_time = datetime.utcnow()
        return self.attendance_repository.save(attendance)

    def lunch_end(self, user_id: int) -> Attendance:
        attendance = self._get_or_create_today_record(user_id)
        if not attendance.lunch_start_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pehle lunch start mark karein")
        if attendance.lunch_end_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Lunch end already mark ho chuka hai")

        attendance.lunch_end_time = datetime.utcnow()
        return self.attendance_repository.save(attendance)

    def check_out(self, user_id: int) -> Attendance:
        attendance = self._get_or_create_today_record(user_id)
        if not attendance.check_in_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Pehle check-in karna zaroori hai")
        if attendance.check_out_time:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Aaj ka check-out already ho chuka hai")

        attendance.check_out_time = datetime.utcnow()
        return self.attendance_repository.save(attendance)

    def get_today_record(self, user_id: int) -> Attendance | None:
        return self.attendance_repository.get_by_user_and_date(user_id, date.today())
