from pydantic import BaseModel, ConfigDict


class CategoryRead(BaseModel):
    id: str
    name: str

    model_config = ConfigDict(from_attributes=True)


class CategoryCreate(BaseModel):
    name: str


class CategoryUpdate(BaseModel):
    name: str | None = None
