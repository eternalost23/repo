from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categories import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id: str) -> CategoryORM | None:
        return self.db.get(CategoryORM, category_id)

    def create(self, name: str) -> CategoryORM:
        new_cat = CategoryORM(name=name)
        self.db.add(new_cat)
        return new_cat

    def update(self, category: CategoryORM, name: str | None) -> CategoryORM:
        if name is not None:
            category.name = name
        return category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(category)
