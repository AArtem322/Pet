from unittest.mock import Mock

import pytest

from app.models.categories import Category
from app.schemas.categories import CategoryCreate, CategoryRead, CategoryUpdate
from app.services.categories import CategoryNotFound, CategoryService


def test_list_categories_returns_pydantic_models(
    service_categories: CategoryService,
    repository_categories_mock: Mock,
) -> None:
    # Имитируем, что метод get_all_categories репозитория вернет эти книги
    repository_categories_mock.get_all_categories.return_value = [
        Category(id="category-1", name="love"),
        Category(id="category-2", name="fantasy"),
    ]

    result = service_categories.get_all_categories()

    assert result == [
        CategoryRead(id="category-1", name="love"),
        CategoryRead(id="category-2", name="fantasy"),
    ]


"""Test CREATE"""


def test_create_category_commits_created_category(
    service_categories: CategoryService,
    db_categories_mock: Mock,
    repository_categories_mock: Mock,
) -> None:
    created_category = Category(id="category-1", name="Новая категория")
    repository_categories_mock.create_category.return_value = created_category

    result = service_categories.create_category(CategoryCreate(name="Новая категория"))

    repository_categories_mock.create_category.assert_called_once_with(
        name="Новая категория"
    )
    db_categories_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": "category-1",
        "name": "Новая категория",
    }


"""Test UPDATE"""


@pytest.mark.parametrize(
    ("payload", "expected_name"),
    [
        pytest.param(
            CategoryUpdate(name="Новая категория"),
            "Новая категория",
        ),
        pytest.param(
            CategoryUpdate(name=None),
            "Старая категория",
        ),
    ],
)
def test_update_category_updates_only_passed_fields(
    service_categories: CategoryService,
    db_categories_mock: Mock,
    repository_categories_mock: Mock,
    payload: CategoryUpdate,
    expected_name: str,
) -> None:
    category = Category(
        id="category-1",
        name="Старая категория",
    )

    repository_categories_mock.get_category_by_id.return_value = category

    result = service_categories.update_category(
        "category-1",
        payload,
    )

    repository_categories_mock.get_category_by_id.assert_called_once_with(
        category_id="category-1"
    )

    db_categories_mock.commit.assert_called_once_with()

    assert result == CategoryRead(
        id="category-1",
        name=expected_name,
    )


"""Test CategoryNotFound"""


def test_update_category_raises_when_category_not_found(
    service_categories: CategoryService,
    db_categories_mock: Mock,
    repository_categories_mock: Mock,
) -> None:
    repository_categories_mock.get_category_by_id.return_value = None

    with pytest.raises(CategoryNotFound):  # Должна произойти указанная ошибка
        service_categories.update_category(
            "missing-category", CategoryUpdate(name="Неважно")
        )

    db_categories_mock.commit.assert_not_called()
