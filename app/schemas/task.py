from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


class TaskSchema(BaseModel):
    """Схема задачи для ответа"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool = False


class TaskCreateSchema(BaseModel):
    title: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)]


class TaskUpdateSchema(BaseModel):
    title: Annotated[
        str | None, StringConstraints(strip_whitespace=True, min_length=1, max_length=255)
    ] = None
    completed: bool | None = None
