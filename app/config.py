from .settins import ApplicationEnvironment, DatabaseSettings


class BaseConfig:
    logging_path: str
    db_host: str
    db_port: int


class LocalConfig(BaseConfig):
    def __int__(self):
        self.logging_path = ''
        self.db_host = DatabaseSettings.db_host
        self.db_port = DatabaseSettings.db_port
