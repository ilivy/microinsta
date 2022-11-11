import logging
import os
from enum import Enum
from functools import lru_cache
from typing import Optional

from pydantic import BaseSettings, PostgresDsn

logger = logging.getLogger(__name__)


class EnvironmentEnum(str, Enum):
    DEV = "dev"
    PROD = "prod"
    

class GlobalConfig(BaseSettings):
    TITLE: str = "Udemyinsta"
    DESCRIPTION: str = "Demo project: FastAPI"

    ENVIRONMENT: EnvironmentEnum
    DEBUG: bool = False
    TIMEZONE: str = "UTC"

    FACE_APP_URL: str = "http://localhost:8081/"
    JWT_SECRET: str = "jwtsecret"

    AWS_ACCESS_KEY: str = ""
    AWS_SECRET_KEY: str = ""
    AWS_BUCKET_PHOTO: str = ""
    AWS_REGION: str = ""

    DATABASE_URL: Optional[
        PostgresDsn
    ] = "postgresql://postgres:postgres@127.0.0.1:5432/postgres"
    DB_ECHO_LOG: bool = False

    @property
    def async_database_url(self) -> Optional[str]:
        return (
            self.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
            if self.DATABASE_URL
            else self.DATABASE_URL
        )

    # Api V1 prefix
    API_V1_STR = "/v1"

    class Config:
        case_sensitive = True


class DevConfig(GlobalConfig):
    """Dev configurations."""

    DEBUG: bool = True
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.DEV


class ProdConfig(GlobalConfig):
    """Prod configurations."""

    DEBUG: bool = False
    ENVIRONMENT: EnvironmentEnum = EnvironmentEnum.PROD


class FactoryConfig:
    def __init__(self, environment: Optional[str]):
        self.environment = environment

    def __call__(self) -> GlobalConfig:
        if self.environment == EnvironmentEnum.DEV.value:
            return DevConfig()
        return ProdConfig()


@lru_cache()
def get_configuration() -> GlobalConfig:
    return FactoryConfig(os.environ.get("ENVIRONMENT"))()


settings = get_configuration()
