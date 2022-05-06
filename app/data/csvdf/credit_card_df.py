import pandas as pd
import numpy as np
from app import settings
from ..utils import aggregate_df


def read_credit_card_csv_data() -> pd.DataFrame:
    card_dtype = {
        'SK_ID_PREV': np.uint32, 'SK_ID_CURR': np.uint32, 'MONTHS_BALANCE': np.int16,
        'AMT_CREDIT_LIMIT_ACTUAL': np.int32, 'CNT_DRAWINGS_CURRENT': np.int32, 'SK_DPD': np.int32,
        'SK_DPD_DEF': np.int32,
        'AMT_BALANCE': np.float32, 'AMT_DRAWINGS_ATM_CURRENT': np.float32, 'AMT_DRAWINGS_CURRENT': np.float32,
        'AMT_DRAWINGS_OTHER_CURRENT': np.float32, 'AMT_DRAWINGS_POS_CURRENT': np.float32,
        'AMT_INST_MIN_REGULARITY': np.float32,
        'AMT_PAYMENT_CURRENT': np.float32, 'AMT_PAYMENT_TOTAL_CURRENT': np.float32,
        'AMT_RECEIVABLE_PRINCIPAL': np.float32,
        'AMT_RECIVABLE': np.float32, 'AMT_TOTAL_RECEIVABLE': np.float32, 'CNT_DRAWINGS_ATM_CURRENT': np.float32,
        'CNT_DRAWINGS_OTHER_CURRENT': np.float32, 'CNT_DRAWINGS_POS_CURRENT': np.float32,
        'CNT_INSTALMENT_MATURE_CUM': np.float32
    }
    card_bal_df = pd.read_csv(f'{settings.DATA_ROOT_PATH}/raw/credit_card_balance.csv', dtype=card_dtype)
    card_bal_df.rename(
        columns={"MONTHS_BALANCE": "MONTHS_BALANCE_CARD", "NAME_CONTRACT_STATUS": "NAME_CONTRACT_STATUS_CARD",
                 "SK_DPD": "SK_DPD_CARD", "SK_DPD_DEF": "SK_DPD_DEF_CARD"}, inplace=True)

    card_group = card_bal_df.groupby('SK_ID_CURR')
    card_number_columns = card_bal_df.dtypes[card_bal_df.dtypes != 'object'].index.tolist()[2:]
    card_bal_df = aggregate_df(card_number_columns, card_group)

    return card_bal_df
