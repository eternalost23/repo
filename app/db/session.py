from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import get_settings

settings = get_settings()
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def get_db():
    """Создаёт сессию БД на время запроса и закрывает её после"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()