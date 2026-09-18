from unittest.mock import Mock

import pytest
from sqlalchemy.orm import Session

from app.repositories.task import TaskRepository
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    """Создаём мок сессии БД один раз и переиспользуем в тестах"""
    return Mock(spec=Session)


@pytest.fixture
def repository_mock() -> Mock:
    """Создаём мок TaskRepository один раз и переиспользуем в тестах"""
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    return TaskService(db_mock, repository_mock)
