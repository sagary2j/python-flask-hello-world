import sqlite3
from contextlib import closing
from datetime import date
from typing import Protocol

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from .config import Settings


class RepositoryError(Exception):
    """The storage backend could not complete the request."""


class UserRepository(Protocol):
    def save(self, username: str, date_of_birth: date) -> None: ...

    def get(self, username: str) -> date | None: ...


class DynamoDBUserRepository:
    def __init__(self, table) -> None:
        self._table = table

    @classmethod
    def from_settings(cls, settings: Settings) -> "DynamoDBUserRepository":
        resource = boto3.resource(
            "dynamodb",
            region_name=settings.aws_region,
            endpoint_url=settings.dynamodb_endpoint_url,
        )
        return cls(resource.Table(settings.table_name))

    def save(self, username: str, date_of_birth: date) -> None:
        try:
            self._table.put_item(
                Item={"username": username, "date_of_birth": date_of_birth.isoformat()}
            )
        except (BotoCoreError, ClientError) as err:
            raise RepositoryError("Failed to save user") from err

    def get(self, username: str) -> date | None:
        try:
            item = self._table.get_item(Key={"username": username}).get("Item")
        except (BotoCoreError, ClientError) as err:
            raise RepositoryError("Failed to load user") from err
        return date.fromisoformat(item["date_of_birth"]) if item else None


class SQLiteUserRepository:
    def __init__(self, path: str) -> None:
        self._path = path
        with closing(self._connect()) as conn, conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS users ("
                "username TEXT PRIMARY KEY, date_of_birth TEXT NOT NULL)"
            )

    def _connect(self) -> sqlite3.Connection:
        return sqlite3.connect(self._path)

    def save(self, username: str, date_of_birth: date) -> None:
        try:
            with closing(self._connect()) as conn, conn:
                conn.execute(
                    "INSERT INTO users (username, date_of_birth) VALUES (?, ?) "
                    "ON CONFLICT(username) DO UPDATE SET date_of_birth = excluded.date_of_birth",
                    (username, date_of_birth.isoformat()),
                )
        except sqlite3.Error as err:
            raise RepositoryError("Failed to save user") from err

    def get(self, username: str) -> date | None:
        try:
            with closing(self._connect()) as conn:
                row = conn.execute(
                    "SELECT date_of_birth FROM users WHERE username = ?", (username,)
                ).fetchone()
        except sqlite3.Error as err:
            raise RepositoryError("Failed to load user") from err
        return date.fromisoformat(row[0]) if row else None


def build_repository(settings: Settings) -> UserRepository:
    if settings.storage_backend == "dynamodb":
        return DynamoDBUserRepository.from_settings(settings)
    if settings.storage_backend == "sqlite":
        return SQLiteUserRepository(settings.sqlite_path)
    raise ValueError(f"Unknown STORAGE_BACKEND: {settings.storage_backend!r}")
