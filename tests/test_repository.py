from datetime import date

import boto3
import pytest
from moto import mock_aws

from app.config import Settings
from app.repository import (
    DynamoDBUserRepository,
    RepositoryError,
    SQLiteUserRepository,
    build_repository,
)


@pytest.fixture
def aws_credentials(monkeypatch):
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "testing")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "testing")


@pytest.fixture
def dynamodb_repository(aws_credentials):
    with mock_aws():
        boto3.client("dynamodb", region_name="us-east-1").create_table(
            TableName="users",
            KeySchema=[{"AttributeName": "username", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "username", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        yield DynamoDBUserRepository.from_settings(Settings())


def test_dynamodb_round_trip(dynamodb_repository):
    assert dynamodb_repository.get("alice") is None
    dynamodb_repository.save("alice", date(1990, 7, 5))
    assert dynamodb_repository.get("alice") == date(1990, 7, 5)


def test_dynamodb_missing_table_raises_repository_error(aws_credentials):
    with mock_aws():
        repository = DynamoDBUserRepository.from_settings(Settings(table_name="missing"))
        with pytest.raises(RepositoryError):
            repository.save("alice", date(1990, 7, 5))
        with pytest.raises(RepositoryError):
            repository.get("alice")


def test_sqlite_round_trip_and_upsert(tmp_path):
    repository = SQLiteUserRepository(str(tmp_path / "users.db"))
    assert repository.get("alice") is None
    repository.save("alice", date(1990, 7, 5))
    repository.save("alice", date(1991, 1, 2))
    assert repository.get("alice") == date(1991, 1, 2)


def test_sqlite_errors_raise_repository_error(tmp_path):
    repository = SQLiteUserRepository(str(tmp_path / "users.db"))
    repository._path = str(tmp_path / "missing-dir" / "users.db")
    with pytest.raises(RepositoryError):
        repository.save("alice", date(1990, 7, 5))
    with pytest.raises(RepositoryError):
        repository.get("alice")


def test_build_repository_selects_backend(tmp_path, aws_credentials):
    settings = Settings(storage_backend="sqlite", sqlite_path=str(tmp_path / "u.db"))
    assert isinstance(build_repository(settings), SQLiteUserRepository)
    assert isinstance(build_repository(Settings()), DynamoDBUserRepository)
    with pytest.raises(ValueError, match="STORAGE_BACKEND"):
        build_repository(Settings(storage_backend="redis"))


def test_settings_from_env(monkeypatch):
    monkeypatch.setenv("STORAGE_BACKEND", "SQLite")
    monkeypatch.setenv("TABLE_NAME", "people")
    monkeypatch.setenv("AWS_REGION", "eu-west-1")
    monkeypatch.setenv("LOG_LEVEL", "debug")
    settings = Settings.from_env()
    assert settings.storage_backend == "sqlite"
    assert settings.table_name == "people"
    assert settings.aws_region == "eu-west-1"
    assert settings.log_level == "DEBUG"
