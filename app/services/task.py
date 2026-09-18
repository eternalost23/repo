import logging

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.task import TaskORM
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema


class TaskNotFound(NotFoundError):
    """Задача не найдена"""


logger = logging.getLogger(__name__)


class TaskService:
    def __init__(self, db: Session, task_repo: TaskRepository) -> None:
        self.db = db
        self.task_repo = task_repo

    def _get_or_raise(self, task_id: str) -> TaskORM:
        task = self.task_repo.get_by_id(task_id)
        if task is None:
            logger.warning("Задача не найдена id=%s", task_id)
            raise TaskNotFound("Задача не найдена")
        return task

    def list_tasks(self) -> list[TaskSchema]:
        tasks = self.task_repo.get_all()
        return [TaskSchema.model_validate(task) for task in tasks]

    def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task = self.task_repo.create(title=task_create.title)
        self.db.commit()
        logger.info("Задача создана id=%s", task.id)
        return TaskSchema.model_validate(task)

    def update_task(self, task_id: str, task_update: TaskUpdateSchema) -> TaskSchema:
        task_for_update = self._get_or_raise(task_id)
        self.task_repo.update(
            task=task_for_update,
            title=task_update.title,
            completed=task_update.completed,
        )
        self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    def delete_task(self, task_id: str) -> None:
        task_for_delete = self._get_or_raise(task_id)
        self.task_repo.delete(task_for_delete)
        self.db.commit()
