from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.books import BookRepository
from app.repositories.categories import CategoryRepository
from app.services.books import BookService
from app.services.categories import CategoryService


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


@pytest.fixture
def db_categories_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


@pytest.fixture
def repository_categories_mock() -> Mock:
    """Создаём мок CategoryRepository один раз и переиспользуем в тестах"""
    return Mock(spec=CategoryRepository)


@pytest.fixture
def service_categories(
    db_categories_mock: Mock, repository_categories_mock: Mock
) -> CategoryService:
    """Создаём CategoryService один раз, чтобы переиспользовать в тестах"""
    category_service = CategoryService(db_categories_mock)
    category_service.categories_repository = repository_categories_mock
    return category_service
