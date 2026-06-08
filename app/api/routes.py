from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_admin
from app.core.database import get_db
from app.model.user import User, UserRole
from app.repository.attendance_repository import AttendanceRepository
from app.repository.task_repository import TaskRepository
from app.repository.user_repository import UserRepository
from app.repository.work_log_repository import WorkLogRepository
from app.schemas.attendance_schemas import AttendanceResponse
from app.schemas.auth_schemas import LoginRequest, TokenResponse
from app.schemas.dashboard_schemas import AdminDashboardSummary, UserTrackingResponse
from app.schemas.task_schemas import TaskCreate, TaskResponse, TaskStatusUpdate
from app.schemas.user_schemas import UserCreate, UserResponse, UserUpdate
from app.schemas.work_log_schemas import WorkLogCreate, WorkLogResponse
from app.services.attendance_service import AttendanceService
from app.services.auth_service import AuthService
from app.services.dashboard_service import DashboardService
from app.services.task_service import TaskService
from app.services.user_service import UserService
from app.services.work_log_service import WorkLogService

router = APIRouter()


@router.post("/auth/bootstrap-admin", response_model=UserResponse, tags=["Auth"])
def bootstrap_admin(payload: UserCreate, db: Session = Depends(get_db)):
    """Project ke first admin ko ek hi baar create karne ke liye route."""
    user_repository = UserRepository(db)
    if user_repository.count_all() > 0:
        raise HTTPException(status_code=403, detail="Bootstrap sirf empty database par allowed hai")

    payload.role = UserRole.ADMIN
    return UserService(user_repository).create_user(payload)


@router.post("/auth/login", response_model=TokenResponse, tags=["Auth"])
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    """User login karke JWT token hasil karta hai."""
    return AuthService(UserRepository(db)).login(payload)


@router.post("/auth/logout", tags=["Auth"])
def logout(current_user: User = Depends(get_current_user)):
    """JWT stateless hota hai, isliye frontend token remove karega."""
    return {"message": f"{current_user.name} successfully logout ho gaye"}


@router.get("/users/me", response_model=UserResponse, tags=["User"])
def get_my_profile(current_user: User = Depends(get_current_user)):
    """Logged-in user apni profile dekh sakta hai."""
    return current_user


@router.post("/attendance/check-in", response_model=AttendanceResponse, tags=["Attendance"])
def check_in(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Din ka start mark karne ke liye check-in route."""
    return AttendanceService(AttendanceRepository(db)).check_in(current_user.id)


@router.post("/attendance/lunch-start", response_model=AttendanceResponse, tags=["Attendance"])
def lunch_start(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lunch break start time mark karta hai."""
    return AttendanceService(AttendanceRepository(db)).lunch_start(current_user.id)


@router.post("/attendance/lunch-end", response_model=AttendanceResponse, tags=["Attendance"])
def lunch_end(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Lunch break end time mark karta hai."""
    return AttendanceService(AttendanceRepository(db)).lunch_end(current_user.id)


@router.post("/attendance/check-out", response_model=AttendanceResponse, tags=["Attendance"])
def check_out(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Din ka final logout/check-out mark karta hai."""
    return AttendanceService(AttendanceRepository(db)).check_out(current_user.id)


@router.get("/attendance/today", response_model=AttendanceResponse | None, tags=["Attendance"])
def get_today_attendance(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Aaj ka attendance status dekhne ke liye."""
    return AttendanceService(AttendanceRepository(db)).get_today_record(current_user.id)


@router.post("/work-logs", response_model=WorkLogResponse, tags=["Work Logs"])
def create_work_log(payload: WorkLogCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee aaj ka kaam aur blockers update karega."""
    return WorkLogService(WorkLogRepository(db)).create_work_log(current_user.id, payload)


@router.get("/work-logs/me", response_model=list[WorkLogResponse], tags=["Work Logs"])
def list_my_work_logs(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logged-in user apne purane work updates dekh sakta hai."""
    return WorkLogService(WorkLogRepository(db)).list_user_work_logs(current_user.id)


@router.get("/tasks/me", response_model=list[TaskResponse], tags=["Tasks"])
def list_my_tasks(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee ke assigned tasks list karta hai."""
    return TaskService(TaskRepository(db), UserRepository(db)).list_user_tasks(current_user.id)


@router.patch("/tasks/{task_id}/status", response_model=TaskResponse, tags=["Tasks"])
def update_my_task_status(task_id: int, payload: TaskStatusUpdate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Employee apne task ka progress status update karega."""
    return TaskService(TaskRepository(db), UserRepository(db)).update_task_status(task_id, current_user.id, payload)


@router.post("/admin/users", response_model=UserResponse, tags=["Admin"])
def create_user(payload: UserCreate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin naya user ya admin create kar sakta hai."""
    return UserService(UserRepository(db)).create_user(payload)


@router.get("/admin/users", response_model=list[UserResponse], tags=["Admin"])
def list_users(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin saare users list kar sakta hai."""
    return UserService(UserRepository(db)).list_users()


@router.patch("/admin/users/{user_id}", response_model=UserResponse, tags=["Admin"])
def update_user(user_id: int, payload: UserUpdate, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin user details update kar sakta hai."""
    return UserService(UserRepository(db)).update_user(user_id, payload)


@router.post("/admin/tasks", response_model=TaskResponse, tags=["Admin"])
def assign_task(payload: TaskCreate, current_admin: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin employee ko naya task assign karega."""
    return TaskService(TaskRepository(db), UserRepository(db)).create_task(current_admin.id, payload)


@router.get("/admin/dashboard", response_model=AdminDashboardSummary, tags=["Admin"])
def get_admin_dashboard(_: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin overview dashboard numbers provide karta hai."""
    service = DashboardService(
        UserRepository(db),
        TaskRepository(db),
        AttendanceRepository(db),
        WorkLogRepository(db),
    )
    return service.get_admin_summary()


@router.get("/admin/users/{user_id}/tracking", response_model=UserTrackingResponse, tags=["Admin"])
def get_user_tracking(user_id: int, _: User = Depends(require_admin), db: Session = Depends(get_db)):
    """Admin ek user ka task, attendance aur work update snapshot dekh sakta hai."""
    user_service = UserService(UserRepository(db))
    task_service = TaskService(TaskRepository(db), UserRepository(db))
    attendance_service = AttendanceService(AttendanceRepository(db))
    work_log_service = WorkLogService(WorkLogRepository(db))

    user = user_service.get_user(user_id)
    today_attendance = attendance_service.get_today_record(user_id)
    work_logs = work_log_service.list_user_work_logs(user_id)[:10]

    return UserTrackingResponse(
        user=user,
        tasks=task_service.list_user_tasks(user_id),
        latest_attendance=today_attendance,
        recent_work_logs=work_logs,
    )
