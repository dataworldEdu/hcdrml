import pandas as pd

from .application_train_df import read_application_train_csv_data
from .previous_application_df import read_previous_application_csv_data
from .bureau_df import read_bureau_csv_data
from .post_cache_df import read_post_cache_csv_data
from .installment_payments_df import read_installment_csv_data
from .credit_card_df import read_credit_card_csv_data


def get_csv_data() -> pd.DataFrame:
    data = read_application_train_csv_data()

    data.merge(read_previous_application_csv_data(), on='SK_ID_CURR', how='left', indicator=True)
    if '_merge' in data.columns:
        del data['_merge']

    data.merge(read_bureau_csv_data(), on='SK_ID_CURR', how='left', indicator=True)
    if '_merge' in data.columns:
        data = data.drop(['_merge'], axis=1)

    data.merge(read_post_cache_csv_data(), on='SK_ID_CURR', how='left', indicator=True)
    if '_merge' in data.columns:
        data = data.drop(['_merge'], axis=1)

    data.merge(read_installment_csv_data(), on='SK_ID_CURR', how='left', indicator=True)
    if '_merge' in data.columns:
        data = data.drop(['_merge'], axis=1)

    data.merge(read_credit_card_csv_data(), on='SK_ID_CURR', how='left', indicator=True)
    if '_merge' in data.columns:
        data = data.drop(['_merge'], axis=1)

    return data


if __name__ == '__main__':
    get_csv_data()
