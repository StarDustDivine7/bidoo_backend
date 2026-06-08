from fastapi import HTTPException, status

from app.model.task import Task
from app.model.user import UserRole
from app.repository.task_repository import TaskRepository
from app.repository.user_repository import UserRepository
from app.schemas.task_schemas import TaskCreate, TaskStatusUpdate


class TaskService:
    """Task assignment aur status update ka business logic."""

    def __init__(self, task_repository: TaskRepository, user_repository: UserRepository):
        self.task_repository = task_repository
        self.user_repository = user_repository

    def create_task(self, admin_user_id: int, payload: TaskCreate) -> Task:
        assignee = self.user_repository.get_by_id(payload.assigned_to_user_id)
        if not assignee:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Assigned user nahi mila")
        if assignee.role != UserRole.EMPLOYEE.value:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Task sirf employee ko assign kiya ja sakta hai",
            )

        task = Task(
            title=payload.title,
            description=payload.description,
            priority=payload.priority.value,
            due_date=payload.due_date,
            assigned_to_user_id=payload.assigned_to_user_id,
            created_by_admin_id=admin_user_id,
        )
        return self.task_repository.create(task)

    def list_user_tasks(self, user_id: int) -> list[Task]:
        return self.task_repository.get_for_user(user_id)

    def update_task_status(self, task_id: int, user_id: int, payload: TaskStatusUpdate) -> Task:
        task = self.task_repository.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task nahi mila")
        if task.assigned_to_user_id != user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Yeh task aapka nahi hai")

        task.status = payload.status.value
        return self.task_repository.save(task)
