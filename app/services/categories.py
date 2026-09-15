from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.models.categories import CategoryORM
from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryCreateSchema, CategoryUpdateSchema


class CategoryNotFound(NotFoundError):
    """Категория не найдена"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.category_repo = CategoryRepository(db)

    def _get_or_raise(self, category_id: str) -> CategoryORM:
        category = self.category_repo.get_by_id(category_id)
        if category is None:
            raise CategoryNotFound("Категория не найдена")
        return category

    def list_categories(self) -> list[CategoryORM]:
        return self.category_repo.get_all()

    def create_category(self, category_create: CategoryCreateSchema) -> CategoryORM:
        category = self.category_repo.create(category_create.name)
        self.db.commit()
        return category

    def update_category(
        self, category_id: str, category_update: CategoryUpdateSchema
    ) -> CategoryORM:
        category_for_update = self._get_or_raise(category_id)
        self.category_repo.update(category=category_for_update, name=category_update.name)
        self.db.commit()
        return category_for_update

    def delete_category(self, category_id: str) -> None:
        category_for_delete = self._get_or_raise(category_id)
        self.category_repo.delete(category_for_delete)
        self.db.commit()
