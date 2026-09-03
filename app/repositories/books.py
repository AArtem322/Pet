from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.books import Book
from app.schemas.books import  BookCreate


class BookRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_books(self):
        return self.db.scalars(select(Book)).all()

    def get_book_by_id(self, book_id: str):
        return self.db.get(Book, book_id)

    def create_book(self, title: str):
        new_book = Book(title=title, is_read=False)
        self.db.add(new_book)
        self.db.commit()
        return new_book

    def delete_book(self, Book) -> None:
        self.db.delete(Book)
        self.db.commit()
