import pandas as pd
import numpy as np
from .utils import min_max_scaler


def nvl(data: pd.DataFrame) -> pd.DataFrame:
    object_col_list = data.dtypes[data.dtypes == 'object'].index.tolist()
    number_col_list = data.dtypes[data.dtypes != 'object'].index.tolist()[2:]

    for col in object_col_list:
        data[col] = data[col].fillna('XX')

    for col in number_col_list:
        data[col] = data[col].fillna(0)

    return data


def one_hot_encoding(data: pd.DataFrame) -> pd.DataFrame:
    encoding_cols = []
    col_index_list = []
    etc_idx=0
    for idx, col in enumerate(data.dtypes[data.dtypes == 'object'].index.tolist()):
        uni_val = data[col].value_counts().index

        for uni_val_idx, val in enumerate(uni_val):
            new_uni_val_col = ''.join([col, '_', uni_val_idx])
            data[new_uni_val_col] = data[col].apply(lambda x: 1 if x == val else 0)
            col_index_list.append([new_uni_val_col, val])
            etc_idx = uni_val_idx + 1

        new_col = ''.join([col, '_', etc_idx])
        data[new_col] = 0
        col_index_list.append([new_col, 0])

        data = data.drop([col], axis=1)
        encoding_cols.append([col, col_index_list])
        # TODO: hot encoding save

    return data


def min_max_scale(data: pd.DataFrame):
    for col in data.dtypes[data.dtypes != 'object'].index.tolist()[2:]:
        data[col] = min_max_scaler(data[col], data[col].max(), data[col].min())
        data[col] = np.log1p(data[col])

