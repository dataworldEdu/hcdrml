import pandas as pd
from app import settings


class SaveParquet:
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        print(self.func.__doc__)
        data = self.func(*args, **kwargs)
        if not isinstance(data, pd.DataFrame):
            raise TypeError("Return type should be Dataframe type~~!!!")
        data.to_parquet(f'{settings.DATA_ROOT_PATH}/processed/data_sample.parquet')
        return data
