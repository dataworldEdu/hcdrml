import unittest
from app.data.ingestion import get_data


class DataTest(unittest.TestCase):

    def test_run(self):
        data = get_data()
        print(data.head(3))
        self.assertIsNotNone(data)
