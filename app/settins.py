from enum import Enum
from pydantic  import BaseSettings, Field, validator


class ApplicationEnvironment(str, Enum):
    LOCAL = 'local'
    DEV = 'dev'
    PROD = 'prod'
    TEST = 'test'


class DatabaseSettings(BaseSettings):
    db_host: str = Field(default="localhost", env="DATABASE_HOST")
    db_port: int = Field(default=3306, env='DATABASE_PORT')

