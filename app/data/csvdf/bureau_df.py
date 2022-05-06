import pandas as pd
import numpy as np
from ..utils import aggregate_df
from app import settings


def read_bureau_csv_data() -> pd.DataFrame():
    bure_col = ['SK_ID_CURR', 'SK_ID_BUREAU', 'CREDIT_ACTIVE', 'CREDIT_CURRENCY', 'DAYS_CREDIT',
                'CREDIT_DAY_OVERDUE'
        , 'DAYS_CREDIT_ENDDATE', 'DAYS_ENDDATE_FACT', 'AMT_CREDIT_MAX_OVERDUE', 'CNT_CREDIT_PROLONG',
                'AMT_CREDIT_SUM'
        , 'AMT_CREDIT_SUM_DEBT', 'AMT_CREDIT_SUM_LIMIT', 'AMT_CREDIT_SUM_OVERDUE', 'CREDIT_TYPE',
                'DAYS_CREDIT_UPDATE', 'AMT_ANNUITY_BRUE']

    bure_dtype = {
        'SK_ID_BUREAU': np.uint32, 'SK_ID_CURR': np.uint32
    }
    bureau_df = pd.read_csv(f'{settings.DATA_ROOT_PATH}/raw/bureau.csv', dtype=bure_dtype)
    bureau_df.columns = bure_col

    bureau_group = bureau_df.groupby('SK_ID_CURR')
    bureau_number_columns = bureau_df.dtypes[bureau_df.dtypes != 'object'].index.tolist()[2:]
    bureau_df = aggregate_df(bureau_number_columns, bureau_group)

    return bureau_df
