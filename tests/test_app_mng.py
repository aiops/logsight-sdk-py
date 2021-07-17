import unittest

from config import PRIVATE_KEY
from logsight.applications import LogsightApplication


class TestAppManagement(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestAppManagement, cls).setUpClass()
        cls.app_mng = LogsightApplication(PRIVATE_KEY)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_create_delete_app(self):
        app_name = 'test_create_app'
        status_code, content = self.app_mng.create(app_name)
        self.assertEqual(status_code, 200)
        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['id'], int)

        status_code, content = self.app_mng.delete(str(content['id']))
        self.assertEqual(status_code, 200)
        self.assertIsInstance(content, dict)
        self.assertTrue('description' in content)

    def test_create_app_invalid_name(self):
        app_name = 'test-create-app'
        with self.assertRaises(SystemExit):
            status_code, content = self.app_mng.create(app_name)
            self.assertEqual(status_code, 400)

    def test_create_duplicate(self):
        app_name = 'test_create_app'
        status_code, content = self.app_mng.create(app_name)
        self.assertEqual(status_code, 200)

        with self.assertRaises(SystemExit):
            status_code, content = self.app_mng.create(app_name)
            self.assertEqual(status_code, 400)

        status_code, content = self.app_mng.delete(str(content['id']))
        self.assertEqual(status_code, 200)
        self.assertTrue('description' in content)

    def test_delete_no_app(self):
        app_id = '0123456789'
        with self.assertRaises(SystemExit):
            status_code, content = self.app_mng.delete(app_id)
            self.assertEqual(status_code, 400)

    def test_list_apps(self):
        n = 3
        app_names = [f'test_create_app_{i}' for i in range(n)]
        app_ids = [self.app_mng.create(app_names[i])[1]['id'] for i in range(n)]

        status_code, content = self.app_mng.lst()
        self.assertEqual(status_code, 200)
        app_list = [(d['id'], d['name']) for d in content]

        self.assertCountEqual(zip(app_ids, app_names), app_list)

        for _id in app_ids:
            status_code, content = self.app_mng.delete(str(_id))
            self.assertEqual(status_code, 200)
            self.assertTrue('description' in content)

    def test_list_apps_empty(self):
        status_code, content = self.app_mng.lst()
        self.assertEqual(status_code, 200)
        self.assertEqual(content, [])


if __name__ == '__main__':
    unittest.main()
