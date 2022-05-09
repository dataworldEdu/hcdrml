import pandas as pd
from app.decorator import SaveParquet
from .csvdf import get_csv_data
from .sqldf import get_sql_data
from ..enums import DataSourceType


@SaveParquet
def get_data(source: DataSourceType = DataSourceType.CSV) -> pd.DataFrame:
    """
    데이터 수집
    :param source:
    :return:
    """
    if source == DataSourceType.SQL:
        return get_sql_data()

    return get_csv_data()
