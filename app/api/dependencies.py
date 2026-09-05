from fastapi import Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.services.books import BookService
from app.services.categories import CategoryService


def get_book_service(db: Session = Depends(get_db)):
    """Функуия для инъекции зависимостей BookService"""
    return BookService(db)


def get_category_service(db: Session = Depends(get_db)):
    """Функуия для инъекции зависимостей CategoryService"""
    return CategoryService(db)
