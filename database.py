from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session

DATABASE_URL = "postgresql+psycopg2://postgres:Artul251220@localhost:5432/postgres"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker[Session](bind=engine)


class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
