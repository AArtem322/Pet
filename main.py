from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

book = ""

class Book(BaseModel):
    title: str


@app.get('/')
def show_book():
    return f"Любимая книга: {book}"

@app.post("/add")
def add(title: Book):
    global book
    book = title.title
    return {
        "title": book,
    }


