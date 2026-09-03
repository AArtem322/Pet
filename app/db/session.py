from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.core.database import DATABASE_URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)


def get_db():
    """Функуия для инъекции сессии Базв Данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
