import pandas as pd
import numpy as np
from ..utils import aggregate_df


def read_previous_application_csv_data() -> pd.DataFrame:
    pre_cols = ['SK_ID_PREV', 'SK_ID_CURR', 'NAME_CONTRACT_TYPE_PRE', 'AMT_ANNUITY_PRE', 'AMT_APPLICATION',
                'AMT_CREDIT_PRE', 'AMT_DOWN_PAYMENT'
        , 'AMT_GOODS_PRICE_PRE', 'WEEKDAY_APPR_PROCESS_START_PRE', 'HOUR_APPR_PROCESS_START_PRE',
                'FLAG_LAST_APPL_PER_CONTRACT', 'NFLAG_LAST_APPL_IN_DAY'
        , 'RATE_DOWN_PAYMENT', 'RATE_INTEREST_PRIMARY', 'RATE_INTEREST_PRIVILEGED', 'NAME_CASH_LOAN_PURPOSE',
                'NAME_CONTRACT_STATUS'
        , 'DAYS_DECISION', 'NAME_PAYMENT_TYPE', 'CODE_REJECT_REASON', 'NAME_TYPE_SUITE_PRE', 'NAME_CLIENT_TYPE',
                'NAME_GOODS_CATEGORY', 'NAME_PORTFOLIO'
        , 'NAME_PRODUCT_TYPE', 'CHANNEL_TYPE', 'SELLERPLACE_AREA', 'NAME_SELLER_INDUSTRY', 'CNT_PAYMENT',
                'NAME_YIELD_GROUP', 'PRODUCT_COMBINATION'
        , 'DAYS_FIRST_DRAWING', 'DAYS_FIRST_DUE', 'DAYS_LAST_DUE_1ST_VERSION', 'DAYS_LAST_DUE', 'DAYS_TERMINATION',
                'NFLAG_INSURED_ON_APPROVAL']

    prev_dtype = {
        'SK_ID_PREV': np.uint32, 'SK_ID_CURR': np.uint32
    }

    prev_app_df = \
        pd.read_csv('/Users/jangsangik/PycharmProjects/hcdrml/data/raw/previous_application.csv', dtype=prev_dtype)
    prev_app_df.columns = pre_cols

    prev_group = prev_app_df.groupby('SK_ID_CURR')
    prev_number_columns = prev_app_df.dtypes[prev_app_df.dtypes != 'object'].index.tolist()[2:]
    prev_app_df = aggregate_df(prev_number_columns, prev_group)

    return prev_app_df


