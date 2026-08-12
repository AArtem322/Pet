from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False)


class Category(Base):
    __tablename__ = "categories"

    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    name: Mapped[str] = mapped_column(nullable=False)
