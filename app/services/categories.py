from sqlalchemy.orm import Session
from app.repositories.categories import CategoryRepository
from app.schemas.categories import CategoryRead, CategoryCreate, CategoryUpdate


class CategoryNotFound(Exception):
    """Категория не найдена"""


class CategoryService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.categories_repository = CategoryRepository(db)

    def get_all_categories(self):
        category_orm = self.categories_repository.get_all_categories()
        return [CategoryRead.model_validate(category) for category in category_orm]

    def create_category(self, category_create: CategoryCreate) -> CategoryRead:
        category_orm = self.categories_repository.create_category(name=category_create.name)
        self.db.commit()
        return CategoryRead.model_validate(category_orm)

    def update_category(self, category_id: str, category_update: CategoryUpdate) -> CategoryRead:
        category_for_update = self.categories_repository.get_category_by_id(category_id=category_id)
        if not category_for_update:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        if category_update.name is not None:
            category_for_update.name = category_update.name
        self.db.commit()
        return CategoryRead.model_validate(category_for_update)

    def delete_category(self, category_id: str):
        category_for_delete = self.categories_repository.get_category_by_id(category_id=category_id)
        if not category_for_delete:
            raise CategoryNotFound(f"Категория с id {category_id} не найдена")
        self.categories_repository.delete_category(category_for_delete)
