import unittest

from config import PRIVATE_KEY
from logsight.applications import LogsightApplication
from logsight.exceptions import LogsightException


class TestAppManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAppManagement, cls).setUpClass()
        cls.app_mng = LogsightApplication(PRIVATE_KEY)

    @classmethod
    def tearDownClass(cls):
        pass

    def _create_app(self, app_name):
        status_code, content = self.app_mng.create(app_name)
        self.assertEqual(status_code, 200)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['id'], int)
        return status_code, content

    def _delete_app(self, app_id):
        status_code, content = self.app_mng.delete(app_id)
        self.assertEqual(status_code, 200)
        self.assertIsInstance(content, dict)
        self.assertTrue('description' in content)
        return status_code, content

    def test_create_delete_app(self):
        app_name = 'test_create_app'
        status_code, content = self._create_app(app_name)
        self._delete_app(str(content['id']))

    def test_create_app_invalid_name(self):
        app_name = 'test-create-app'
        with self.assertRaises(LogsightException):
            status_code, content = self.app_mng.create(app_name)
            self.assertEqual(status_code, 400)

    def test_create_duplicate(self):
        app_name = 'test_create_app'
        _, content = self._create_app(app_name)

        with self.assertRaises(LogsightException):
            status_code, content = self.app_mng.create(app_name)
            self.assertEqual(status_code, 400)

        self._delete_app(str(content['id']))

    def test_delete_no_app(self):
        app_id = '0123456789'
        with self.assertRaises(LogsightException):
            status_code, content = self.app_mng.delete(app_id)
            self.assertEqual(status_code, 400)

    def test_create_list_delete_apps(self):
        n = 10
        app_names = [f'test_create_app_{i}' for i in range(n)]
        app_ids = [self._create_app(app_name)[1]['id'] for app_name in app_names]

        status_code, content = self.app_mng.lst()
        self.assertEqual(status_code, 200)
        app_list = [(d['id'], d['name']) for d in content if 'test_create_app_' in d['name']]

        self.assertCountEqual(zip(app_ids, app_names), app_list)

        for _id in app_ids:
            self._delete_app(str(_id))

    def test_list_apps_empty(self):
        status_code, content = self.app_mng.lst()
        self.assertEqual(status_code, 200)
        self.assertEqual(content, [])


if __name__ == '__main__':
    unittest.main()
