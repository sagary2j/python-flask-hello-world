from datetime import date

import pytest

from app import create_app
from app.config import Settings
from app.repository import RepositoryError

TODAY = date(2026, 6, 30)


class InMemoryUserRepository:
    def __init__(self) -> None:
        self.users: dict[str, date] = {}

    def save(self, username: str, date_of_birth: date) -> None:
        self.users[username] = date_of_birth

    def get(self, username: str) -> date | None:
        return self.users.get(username)


class FailingUserRepository:
    def save(self, username: str, date_of_birth: date) -> None:
        raise RepositoryError("boom: arn:aws:dynamodb:secret-detail")

    def get(self, username: str) -> date | None:
        raise RepositoryError("boom: arn:aws:dynamodb:secret-detail")


@pytest.fixture
def repository() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def client(repository):
    app = create_app(settings=Settings(), repository=repository, today=lambda: TODAY)
    return app.test_client()


@pytest.fixture
def failing_client():
    app = create_app(settings=Settings(), repository=FailingUserRepository(), today=lambda: TODAY)
    return app.test_client()
