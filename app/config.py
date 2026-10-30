import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    storage_backend: str = "dynamodb"
    table_name: str = "users"
    aws_region: str = "us-east-1"
    dynamodb_endpoint_url: str | None = None
    sqlite_path: str = "users.db"
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "Settings":
        return cls(
            storage_backend=os.getenv("STORAGE_BACKEND", cls.storage_backend).lower(),
            table_name=os.getenv("TABLE_NAME", cls.table_name),
            aws_region=os.getenv("AWS_REGION", os.getenv("AWS_DEFAULT_REGION", cls.aws_region)),
            dynamodb_endpoint_url=os.getenv("DYNAMODB_ENDPOINT_URL") or None,
            sqlite_path=os.getenv("SQLITE_PATH", cls.sqlite_path),
            log_level=os.getenv("LOG_LEVEL", cls.log_level).upper(),
        )
