import os
from pathlib import Path
from pydantic import BaseSettings


class GlobalSettings(BaseSettings):
    APP_ENV: str = 'local'


class LocalSettings(GlobalSettings):
    LOGGING_PATH: str = ''
    DB_HOST: str = ''
    DB_PORT: str = ''
    APP_ROOT_PATH: str = os.path.dirname(os.path.abspath(Path(__file__).parent))
    DATA_ROOT_PATH: str = f'{APP_ROOT_PATH}/data/'
    MODEL_FILE_ROOT_PATH: str = f'{APP_ROOT_PATH}/models/'


class DevSettings(GlobalSettings):
    LOGGING_PATH: str
    DB_HOST: str
    DB_PORT: str
    APP_ROOT_PATH: str
    DATA_ROOT_PATH: str
    MODEL_FILE_ROOT_PATH: str


class ProdSettings(GlobalSettings):
    LOGGING_PATH: str
    DB_HOST: str
    DB_PORT: str
    APP_ROOT_PATH: str
    DATA_ROOT_PATH: str
    MODEL_FILE_ROOT_PATH: str


class FactorySettings:
    @staticmethod
    def load():
        app_env = GlobalSettings().APP_ENV
        if app_env == 'local':
            return LocalSettings()

        elif app_env == 'dev':
            return DevSettings()

        elif app_env == 'prod':
            return ProdSettings()


settings = FactorySettings.load()
