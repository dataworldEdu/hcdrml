import pandas as pd
from .csvdf import get_csv_data
from .sqldf import get_sql_data
from ..enums import DataSourceType


def get_data(source: DataSourceType = DataSourceType.CSV) -> pd.DataFrame:
    if source == DataSourceType.SQL:
        return get_sql_data()

    return get_csv_data()
