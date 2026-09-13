from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from app.db.session import engine
from app.models.base import Base
from app.api.routers.task import router as task_router 

@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router=task_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


# @app.get("/categories", response_model=list[Category])
# def get_categories(db: Session = Depends(get_db)):
#     """Получить список категорий"""
#     return db.scalars(select(CategoryORM)).all()


# @app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
# def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
#     """Создать категорию"""
#     category = CategoryORM(name=payload.name)
#     db.add(category)
#     db.commit()
#     db.refresh(category)
#     return category


# @app.patch("/categories/{category_id}", response_model=Category)
# def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
#     """Частично обновить категорию"""
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

#     if payload.name is not None:
#         category.name = payload.name

#     db.commit()
#     db.refresh(category)
#     return category


# @app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
#     """Удалить категорию"""
#     category = db.get(CategoryORM, category_id)
#     if category is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

#     db.delete(category)
#     db.commit()