from pydantic import BaseModel


class BookRead(BaseModel):
    id: str
    title: str
    is_read: bool

class BookCreate(BaseModel):
    title: str


class BookUpdate(BaseModel):
    title: str | None=None
    is_read: bool | None=None

class CategoryRead(BaseModel):
    id: str
    name: str


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None=None
