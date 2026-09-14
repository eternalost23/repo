from sqlalchemy.orm import Mapped

from app.models.base import Base


class CategoryORM(Base):
    """Модель для таблицы категорий"""

    __tablename__ = "categories"

    name: Mapped[str]
