from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import get_db
from models import Book, Category
from schemas import CategoryCreate, CategoryUpdate


def show_all_categories(db: Session = Depends(get_db())):
    query = select(Category)
    categories = db.scalars(query).all()
    return categories

def create_new_category(category: CategoryCreate, db: Session = Depends(get_db)):
    category = Category(name=category.name)
    db.add(category)
    db.commit()
    db.refresh(category)
    return category

# def update_category(category_id, name, db: Session = Depends(get_db)):
#     query = select(Category).where(Category.id == category_id)
#     category = db.scalar(query)
#     category.name = name
#     db.commit()
#     db.refresh(category)
#     return category
#
#
# def delete_category(category: Category, category_id, db: Session = Depends(get_db)):
#     query = select(Category).where(Category.id == category_id)
#     for category in query:
#         if category.id == category_id:
#             db.delete(category)
#             db.refresh(category)
#             db.commit()
#         raise HTTPException(status_code=404, detail="Категория не найдена")