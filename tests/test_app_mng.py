import unittest
import requests

from config import PRIVATE_KEY, APP_NAME, DELAY_TO_QUERY_BACKEND
from logsight.applications import LogsightApplication


# unittest.TestLoader.sortTestMethodsUsing = lambda self, a, b: (a < b) - (a > b)


class TestAppManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAppManagement, cls).setUpClass()
        cls.app_mng = LogsightApplication(PRIVATE_KEY)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_delete_app(self):
        app_name = 'test_create_app11'
        result = self.app_mng.create(app_name)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['id'], int)

        # result = self.app_mng.delete(str(result['id']))
        # self.assertEqual(result, 'OK')
        # if app exists,
        # 409 Conflict - if the server will not process a request, but the reason for that is not the client's

    # def test_create_duplicate(self):
    #     app_name = 'test_create_app_2'
    #     result = self.app_mng.create(app_name)
    #     self.assertRaises(SystemExit, lambda: self.app_mng.create(app_name))
    #
    #     result = self.app_mng.delete(str(result['id']))
    #     self.assertEqual(result, 'OK')


if __name__ == '__main__':
    unittest.main()
