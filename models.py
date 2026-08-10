from pydantic import BaseModel


class Book(BaseModel):
    id: str
    title: str
    is_read: bool


class Category(BaseModel):
    id: str
    name: str
