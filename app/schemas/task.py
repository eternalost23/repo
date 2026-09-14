from pydantic import BaseModel, ConfigDict, Field


class TaskSchema(BaseModel):
    """Схема задачи для ответа"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool = False


class TaskCreateSchema(BaseModel):
    title: str = Field(min_length=1, max_length=255)


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=255)
    completed: bool | None = None
