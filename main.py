from contextlib import asynccontextmanager
from models import Category, Book
from services import books as books_service
from services import categories as categories_service
from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import *


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.get('/books')
def show_all_books(db: Session = Depends(get_db)):
    books = books_service.get_all_books(db)
    return books


@app.get("/categories")
def show_categories(db: Session = Depends(get_db)):
    categories = categories_service.show_all_categories(db)
    return categories


@app.post('/add/book', status_code=status.HTTP_201_CREATED)
def add_book(payload: BookCreate, db: Session = Depends(get_db)) -> BookRead:
    book = books_service.add_book(payload, db)
    return book


@app.post('/add/categories', status_code=status.HTTP_201_CREATED)
def add_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategoryRead:
    category = categories_service.create_new_category(payload, db)
    return category


@app.patch('/books/{book_id}')
def update_book(book_id: str, payload: BookUpdate, db: Session = Depends(get_db)):
    book_for_update = db.get(Book, book_id)
    if book_for_update:
        if payload.title:
            book_for_update.title = payload.title
        if payload.is_read:
            book_for_update.is_read = payload.is_read
        db.commit()
        return book_for_update
    raise HTTPException(status_code=404, detail="Book not found")


@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate, db: Session = Depends(get_db)):
    category_for_update = db.get(Category, category_id)
    if category_for_update:
        if payload.name:
            category_for_update.name = payload.name
        db.commit()
        return category_for_update
    raise HTTPException(status_code=404, detail="Category not found")


@app.delete('/books/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id, db: Session = Depends(get_db)):
    book_for_delete = db.get(Book, book_id)
    if book_for_delete:
        db.delete(book_for_delete)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Book not found")


@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id, db: Session = Depends(get_db)):
    category_for_delete = db.get(Category, category_id)
    if category_for_delete:
        db.delete(category_for_delete)
        db.commit()
        return
    raise HTTPException(status_code=404, detail="Category not found")
