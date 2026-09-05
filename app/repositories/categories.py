from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.categories import Category


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all_categories(self):
        return self.db.scalars(select(Category)).all()

    def get_category_by_id(self, category_id: str):
        return self.db.get(Category, category_id)

    def create_category(self, name: str):
        new_category = Category(name=name)
        self.db.add(new_category)
        self.db.commit()
        return new_category

    def delete_category(self, Category):
        self.db.delete(Category)
        self.db.commit()
