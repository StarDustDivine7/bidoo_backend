from datetime import date, datetime

from pydantic import BaseModel, ConfigDict


class AttendanceResponse(BaseModel):
    """Attendance record ka safe response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    attendance_date: date
    check_in_time: datetime | None = None
    lunch_start_time: datetime | None = None
    lunch_end_time: datetime | None = None
    check_out_time: datetime | None = None
    created_at: datetime
    updated_at: datetime
