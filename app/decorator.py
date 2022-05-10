import pandas as pd
from functools import wraps
from app import settings


def save_parquet(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(func.__doc__)
        data = func(*args, **kwargs)
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Return type should be Dataframe type~~!!!")
        data.to_parquet(f'{settings.DATA_ROOT_PATH}/processed/data_sample.parquet')
        return data

    return wrapper
