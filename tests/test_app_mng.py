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
        app_name = 'testCreateApp'
        result = self.app_mng.create(app_name)
        self.assertIsInstance(result, dict)
        self.assertIsInstance(result['id'], int)

        result = self.app_mng.delete(str(result['id']))
        self.assertIsInstance(result, dict)
        self.assertTrue('description' in result)

    def test_create_duplicate(self):
        app_name = 'testCreateApp'
        result = self.app_mng.create(app_name)
        self.assertRaises(SystemExit, lambda: self.app_mng.create(app_name))

        result = self.app_mng.delete(str(result['id']))
        self.assertTrue('description' in result)

    def test_delete_no_app(self):
        app_id = '0123456789'
        self.assertRaises(SystemExit, lambda: self.app_mng.delete(app_id))

    def test_list_apps(self):
        n = 3
        app_names = [f'testCreateApp{i}' for i in range(n)]
        app_ids = [self.app_mng.create(app_names[i])['id'] for i in range(n)]

        app_list = [(d['id'], d['name']) for d in self.app_mng.lst()]

        self.assertCountEqual(zip(app_ids, app_names), app_list)

        for _id in app_ids:
            result = self.app_mng.delete(str(_id))
            self.assertTrue('description' in result)

    def test_list_apps_empty(self):
        self.assertEqual(self.app_mng.lst(), [])


if __name__ == '__main__':
    unittest.main()
