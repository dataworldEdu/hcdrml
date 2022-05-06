from enum import Enum


class DataSourceType(str, Enum):
    CSV = 'csv'
    SQL = 'sql'
    PICKLE = 'pickle'
    JSON = 'json'
    DATAFRAME = 'dataframe'
