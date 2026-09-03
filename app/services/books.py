from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.repositories.books import BookRepository
from app.schemas.books import BookCreate, BookRead, BookUpdate


class BookNotFound(Exception):
    """Задача не найдена"""


class BookService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.books_repository = BookRepository(db)

    def get_all_books(self):
        book_orm = self.books_repository.get_all_books()
        return [BookRead.model_validate(book) for book in book_orm]

    def create_book(self, book_create: BookCreate) -> BookRead:
        book_orm = self.books_repository.create_book(title=book_create.title)
        self.db.commit()
        return BookRead.model_validate(book_orm)

    def update_book(self, book_id: str, book_update: BookUpdate) -> BookRead:
        book_for_update = self.books_repository.get_book_by_id(book_id=book_id)
        if not book_for_update:
            raise BookNotFound(f"Задача с id {book_id} не найдена")
        if book_update.title is not None:
            book_for_update.title = book_update.title
        if book_update.is_read is not None:
            book_for_update.is_read = book_update.is_read
        self.db.commit()
        return BookRead.model_validate(book_for_update)

    def delete_book(self, book_id: str):
        book_for_delete = self.books_repository.get_book_by_id(book_id=book_id)
        if not book_for_delete:
            raise BookNotFound(f"Задача с id {book_id} не найдена")
        self.books_repository.delete_book(book_for_delete)
