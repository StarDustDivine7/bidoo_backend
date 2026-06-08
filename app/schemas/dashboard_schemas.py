from pydantic import BaseModel

from app.schemas.attendance_schemas import AttendanceResponse
from app.schemas.task_schemas import TaskResponse
from app.schemas.user_schemas import UserResponse
from app.schemas.work_log_schemas import WorkLogResponse


class AdminDashboardSummary(BaseModel):
    """Admin ke overview dashboard ka compact summary."""

    total_users: int
    total_admins: int
    total_employees: int
    active_users: int
    open_tasks: int
    completed_tasks: int
    today_attendance_marked: int
    today_work_updates: int


class UserTrackingResponse(BaseModel):
    """Admin ko ek user ka complete tracking snapshot dikhata hai."""

    user: UserResponse
    tasks: list[TaskResponse]
    latest_attendance: AttendanceResponse | None = None
    recent_work_logs: list[WorkLogResponse]
