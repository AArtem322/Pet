from starlette import status
from fastapi import APIRouter, Depends, HTTPException

from app.schemas.books import BookUpdate, BookRead, BookCreate
from app.api.dependencies import get_book_service
from app.services.books import BookService, BookNotFound

router = APIRouter(prefix="/books", tags=["Books"])


@router.get('/')
def show_all_books(book_service: BookService = Depends(get_book_service)):
    return book_service.get_all_books()


@router.post('/create', status_code=status.HTTP_201_CREATED)
def create_book(
        payload: BookCreate,
        book_service: BookService = Depends(get_book_service)
) -> BookRead:
    return book_service.create_book(book_create=payload)


@router.patch('/{book_id}')
def update_book(
        book_id: str,
        payload: BookUpdate,
        book_service: BookService = Depends(get_book_service)
) -> BookRead:
    try:
        return book_service.update_book(book_id=book_id, book_update=payload)
    except BookNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@router.delete('/{book_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: str, book_service: BookService = Depends(get_book_service)):
    try:
        return book_service.delete_book(book_id=book_id)
    except BookNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)