from app.settings import settings
import unittest


class SettingsTest(unittest.TestCase):

    def test_runs(self):
        print(settings.dict())
        self.assertIsNotNone(config.APP_ROOT)
