from csvdf import get_csv_data
from sqldf import get_sql_data


def get_data(args: str):
    if args == 'sql':
        return get_sql_data()

    return get_csv_data()
