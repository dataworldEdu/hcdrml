import unittest
import pandas as pd
from pandas.util.testing import assert_frame_equal
from app.data.ingestion import get_data


class PyArrowTest(unittest.TestCase):

    def test_save_df(self):
        df = get_data()
        df.to_parquet('/Users/jangsangik/PycharmProjects/hcdrml/data/processed/data_pa.parquet', 'pyarrow')
        print('save completed~!!!')

    def test_assert_dataframe(self):
        data_df = get_data()
        file_df = pd.read_parquet('/Users/jangsangik/PycharmProjects/hcdrml/data/processed/data_pa.parquet')
        self.assertIsNone(assert_frame_equal(data_df, file_df))
        print('df same~!!!')
