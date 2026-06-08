from datetime import date

from app.model.user import UserRole
from app.repository.attendance_repository import AttendanceRepository
from app.repository.task_repository import TaskRepository
from app.repository.user_repository import UserRepository
from app.repository.work_log_repository import WorkLogRepository
from app.schemas.dashboard_schemas import AdminDashboardSummary


class DashboardService:
    """Admin dashboard ke aggregate numbers yaha calculate hote hain."""

    def __init__(
        self,
        user_repository: UserRepository,
        task_repository: TaskRepository,
        attendance_repository: AttendanceRepository,
        work_log_repository: WorkLogRepository,
    ):
        self.user_repository = user_repository
        self.task_repository = task_repository
        self.attendance_repository = attendance_repository
        self.work_log_repository = work_log_repository

    def get_admin_summary(self) -> AdminDashboardSummary:
        today = date.today()
        return AdminDashboardSummary(
            total_users=self.user_repository.count_all(),
            total_admins=self.user_repository.count_by_role(UserRole.ADMIN),
            total_employees=self.user_repository.count_by_role(UserRole.EMPLOYEE),
            active_users=self.user_repository.count_active(),
            open_tasks=self.task_repository.count_open_tasks(),
            completed_tasks=self.task_repository.count_completed_tasks(),
            today_attendance_marked=self.attendance_repository.count_marked_for_date(today),
            today_work_updates=self.work_log_repository.count_for_date(today),
        )
