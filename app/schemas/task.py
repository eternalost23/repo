from pydantic import BaseModel, ConfigDict


class TaskSchema(BaseModel):
    """Схема задачи для ответа"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool = False


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    """Схема категории для ответа"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None