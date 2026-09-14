from pydantic import BaseModel, ConfigDict, Field


class CategorySchema(BaseModel):
    """Схема категории для ответа"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=255)


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
