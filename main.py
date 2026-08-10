from fastapi import FastAPI, HTTPException, status
from uuid import uuid4
from schemas import *

app = FastAPI()

books: list[BookRead] = []

categories: list[CategoryRead] = []


@app.get('/books')
def show_book() -> str:
    return f"Любимая книга: {books}"


@app.get("/categories")
def show_category():
    return f"Список категорий: {categories}"


@app.post('/add/book', status_code=status.HTTP_201_CREATED)
def add_book(payload: BookCreate) -> BookRead:
    new_book = BookRead(id=str(uuid4()), title=payload.title, is_read=False)
    books.append(new_book)
    return new_book


@app.post('/add/categories', status_code=status.HTTP_201_CREATED)
def add_category(payload: CategoryCreate) -> CategoryRead:
    new_category = CategoryRead(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category

@app.patch('/categories/{category_id}')
def update_category(category_id: str, payload: CategoryUpdate):
    for category in categories:
        if category.id == category_id:
            category.name = payload.name
            return category
        raise HTTPException(status_code=404)

@app.delete('/categories/{category_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return category
        raise HTTPException(status_code=404)

