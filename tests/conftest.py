from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.books import BookRepository
from app.services.books import BookService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок BookRepository один раз и переиспользуем в тестах"""
    return Mock(spec=BookRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> BookService:
    """Создаём BookService один раз, чтобы переиспользовать в тестах"""
    book_service = BookService(db_mock)
    book_service.books_repository = repository_mock
    return book_service
