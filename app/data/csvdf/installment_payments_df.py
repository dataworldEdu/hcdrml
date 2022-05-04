import pandas as pd
import numpy as np
from ..utils import aggregate_df


def read_installment_csv_data() -> pd.DataFrame():
    install_dtype = {
        'SK_ID_PREV': np.uint32, 'SK_ID_CURR': np.uint32, 'NUM_INSTALMENT_NUMBER': np.int32,
        'NUM_INSTALMENT_VERSION': np.float32,
        'DAYS_INSTALMENT': np.float32, 'DAYS_ENTRY_PAYMENT': np.float32, 'AMT_INSTALMENT': np.float32,
        'AMT_PAYMENT': np.float32
    }

    install_df= pd.read_csv('/Users/jangsangik/PycharmProjects/hcdrml/data/raw/installments_payments.csv',
                               dtype=install_dtype)

    install_group = install_df.groupby('SK_ID_CUPR')
    install_number_columns = install_df.dtypes[install_df.dtypes != 'object'].index.tolist()[2:]

    install_df = aggregate_df(install_number_columns, install_group)

    return install_df
    