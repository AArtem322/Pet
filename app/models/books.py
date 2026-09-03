from uuid import uuid4

from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Book(Base):
    __tablename__ = "books"
    id: Mapped[str] = mapped_column(primary_key=True, default=lambda: str(uuid4()))
    title: Mapped[str] = mapped_column(nullable=False)
    is_read: Mapped[bool] = mapped_column(default=False)