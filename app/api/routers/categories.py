from fastapi import APIRouter, status

from app.api.dependencies import CategoryServiceDep
from app.schemas.categories import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)

router = APIRouter(prefix="/categories")


@router.get("", response_model=list[CategorySchema])
def get_categories(category_service: CategoryServiceDep):
    return category_service.list_categories()


@router.post("", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema,
    category_service: CategoryServiceDep,
):
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}", response_model=CategorySchema)
def update_category(
    category_id: str,
    payload: CategoryUpdateSchema,
    category_service: CategoryServiceDep,
):
    return category_service.update_category(
        category_id=category_id, category_update=payload
    )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, category_service: CategoryServiceDep) -> None:
    category_service.delete_category(category_id)
