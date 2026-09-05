from unittest.mock import Mock

import pytest

from app.models.books import Book
from app.schemas.books import BookCreate, BookRead, BookUpdate
from app.services.books import BookNotFound, BookService


def test_list_books_returns_pydantic_models(
    service: BookService,
    repository_mock: Mock,
) -> None:
    # Имитируем, что метод get_all_books репозитория вернет эти книги
    repository_mock.get_all_books.return_value = [
        Book(id="book-1", title="Evgeniy Onegin", is_read=False),
        Book(id="book-2", title="Война и Мир", is_read=True),
    ]

    result = service.get_all_books()

    assert result == [
        BookRead(id="book-1", title="Evgeniy Onegin", is_read=False),
        BookRead(id="book-2", title="Война и Мир", is_read=True),
    ]


"""Test CREATE"""


def test_create_book_commits_created_book(
    service: BookService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    created_book = Book(id="book-1", title="Новая книга", is_read=False)
    repository_mock.create_book.return_value = created_book

    result = service.create_book(BookCreate(title="Новая книга"))

    repository_mock.create_book.assert_called_once_with(title="Новая книга")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "book-1",
        "title": "Новая книга",
        "is_read": False,
    }


"""Test UPDATE"""


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_is_read"),
    [
        pytest.param(
            BookUpdate(title="Обновить название"),  # payload
            "Обновить название",  # expected_title
            False,  # expected_completed
        ),
        pytest.param(
            BookUpdate(is_read=True),  # payload
            "Старая книга",  # expected_title
            True,  # expected_completed
        ),
        pytest.param(
            BookUpdate(title="Готово", is_read=True),  # payload
            "Готово",  # expected_title
            True,  # expected_completed
        ),
    ],
)
def test_update_book_updates_only_passed_fields(
    service: BookService,
    db_mock: Mock,
    repository_mock: Mock,
    payload: BookUpdate,
    expected_title: str,
    expected_is_read: bool,
) -> None:
    book = Book(id="book-1", title="Старая книга", is_read=False)
    repository_mock.get_book_by_id.return_value = book

    result = service.update_book("book-1", payload)

    repository_mock.get_book_by_id.assert_called_once_with(book_id="book-1")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "book-1",
        "title": expected_title,
        "is_read": expected_is_read,
    }


"""Test BookNotFound"""


def test_update_book_raises_when_book_not_found(
    service: BookService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    repository_mock.get_book_by_id.return_value = None

    with pytest.raises(BookNotFound):  # Должна произойти указанная ошибка
        service.update_book("missing-book", BookUpdate(title="Неважно"))

    db_mock.commit.assert_not_called()
