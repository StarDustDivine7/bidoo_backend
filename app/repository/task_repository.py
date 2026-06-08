from sqlalchemy.orm import Session

from app.model.task import Task, TaskStatus


class TaskRepository:
    """Task related DB queries ko centralize karta hai."""

    def __init__(self, db: Session):
        self.db = db

    def create(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def get_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_for_user(self, user_id: int) -> list[Task]:
        return self.db.query(Task).filter(Task.assigned_to_user_id == user_id).order_by(Task.created_at.desc()).all()

    def count_open_tasks(self) -> int:
        return self.db.query(Task).filter(Task.status != TaskStatus.COMPLETED.value).count()

    def count_completed_tasks(self) -> int:
        return self.db.query(Task).filter(Task.status == TaskStatus.COMPLETED.value).count()

    def save(self, task: Task) -> Task:
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task
