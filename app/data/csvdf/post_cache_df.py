import pandas as pd
import numpy as np
from app import settings
from ..utils import aggregate_df


def read_post_cache_csv_data() -> pd.DataFrame():
    pos_dtype = {
        'SK_ID_PREV': np.uint32, 'SK_ID_CURR': np.uint32, 'MONTHS_BALANCE': np.int32, 'SK_DPD': np.int32,
        'SK_DPD_DEF': np.int32, 'CNT_INSTALMENT': np.float32, 'CNT_INSTALMENT_FUTURE': np.float32
    }
    post_cash_bal_df = pd.read_csv(f'{settings.DATA_ROOT_PATH}/raw/POS_CASH_balance.csv', dtype=pos_dtype)

    pos_group = post_cash_bal_df.groupby('SK_ID_CURR')
    pos_number_columns = post_cash_bal_df.dtypes[post_cash_bal_df.dtypes != 'object'].index.tolist()[2:]
    post_cash_bal_df = aggregate_df(pos_number_columns, pos_group)

    return post_cash_bal_df
