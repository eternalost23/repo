from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.categories import CategoryService
from app.services.task import TaskService

DbSession = Annotated[Session, Depends(get_db)]


def get_task_service(db: DbSession) -> TaskService:
    return TaskService(db)


def get_category_service(db: DbSession) -> CategoryService:
    return CategoryService(db)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
