from pydantic import BaseModel, ConfigDict


class BookRead(BaseModel):
    id: str
    title: str
    is_read: bool

    model_config = ConfigDict(from_attributes=True)

class BookCreate(BaseModel):
    title: str


class BookUpdate(BaseModel):
    title: str | None=None
    is_read: bool | None=None