from fastapi import APIRouter, Depends, HTTPException
from starlette import status

from app.api.dependencies import get_category_service
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.categories import CategoryNotFound, CategoryService

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/")
def show_all_categories(
    category_service: CategoryService = Depends(get_category_service),
):
    return category_service.get_all_categories()


@router.post("/create", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreate,
    category_service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}")
def update_category(
    category_id: str,
    payload: CategoryUpdate,
    category_service: CategoryService = Depends(get_category_service),
) -> CategoryRead:
    try:
        return category_service.update_category(
            category_id=category_id, category_update=payload
        )
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: str, category_service: CategoryService = Depends(get_category_service)
):
    try:
        return category_service.delete_category(category_id=category_id)
    except CategoryNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
