from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from database import get_db
from models import Book
from schemas import BookCreate


def get_all_books(db: Session = Depends(get_db())):
    query = select(Book)
    books = db.scalars(query).all()
    return books


def add_book(book_data: BookCreate, db: Session = Depends(get_db())):
    book = Book(title=book_data.title)
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


def get_book_by_id(book_id: str, db: Session = Depends(get_db)):
    book = db.get(Book, book_id)
    return book


def delete_book(book: Book, db: Session = Depends(get_db)):
    db.delete(book)
    db.commit()


def toggle_book(book: Book, db: Session = Depends(get_db)):
    book.is_read = not book.is_read
    db.commit()
    db.refresh(book)
    return book
