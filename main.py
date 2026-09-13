from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:5433/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


class Base(DeclarativeBase):
    """Базовый класс для всех моделей таблиц БД"""
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))


class TaskORM(Base):
    """Модель для таблицы задач"""
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    """Модель для таблицы категорий"""
    __tablename__ = "categories"

    name: Mapped[str]


class Task(BaseModel):
    """Схема задачи для ответа"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    title: str
    completed: bool = False


class TaskCreate(BaseModel):
    title: str


class TaskUpdate(BaseModel):
    title: str | None = None
    completed: bool | None = None


class Category(BaseModel):
    """Схема категории для ответа"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


def get_db():
    """Создаёт сессию БД на время запроса и закрывает её после"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/tasks", response_model=list[Task])
def get_tasks(db: Session = Depends(get_db)):
    """Получить список задач"""
    return db.scalars(select(TaskORM)).all()


@app.post("/tasks", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate, db: Session = Depends(get_db)):
    """Создать задачу"""
    task = TaskORM(title=payload.title)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


@app.patch("/tasks/{task_id}", response_model=Task)
def update_task(task_id: str, payload: TaskUpdate, db: Session = Depends(get_db)):
    """Частично обновить задачу"""
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    if payload.title is not None:
        task.title = payload.title
    if payload.completed is not None:
        task.completed = payload.completed

    db.commit()
    db.refresh(task)
    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: Session = Depends(get_db)) -> None:
    """Удалить задачу"""
    task = db.get(TaskORM, task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()



@app.get("/categories", response_model=list[Category])
def get_categories(db: Session = Depends(get_db)):
    """Получить список категорий"""
    return db.scalars(select(CategoryORM)).all()


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreate, db: Session = Depends(get_db)):
    """Создать категорию"""
    category = CategoryORM(name=payload.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@app.patch("/categories/{category_id}", response_model=Category)
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    """Частично обновить категорию"""
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    if payload.name is not None:
        category.name = payload.name

    db.commit()
    db.refresh(category)
    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: Session = Depends(get_db)) -> None:
    """Удалить категорию"""
    category = db.get(CategoryORM, category_id)
    if category is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")

    db.delete(category)
    db.commit()