

from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema

class TaskNotFound(Exception):
     """Задача не найдена"""

class TaskService:
    def __init__(self, db: Session)-> None:
        self.db =db
        self.task_repo = TaskRepository(db)

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.task_repo.get_all()
        return tasks

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task = self.task_repo.create(title=task_create.title)
        self.db.commit()
        return task

    def update_task(self, task_id, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self.task_repo.get_by_id(task_id)
        if task_for_update is None:
            raise TaskNotFound("Задача не найдена")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        self.db.commit()
        return task_for_update

    def delete_task(self, task_id: str) -> TaskSchema:
        task_for_delete = self.task_repo.get_by_id(task_id)
        if task_for_delete is None:
            raise TaskNotFound("Задача не найдена")
        self.task_repo.delete(task_for_delete)
        self.db.commit()