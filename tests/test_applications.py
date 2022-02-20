import unittest

from config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound)


class TestAppManagement(unittest.TestCase):

    app_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestAppManagement, cls).setUpClass()
        u = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(u.user_id, u.token)
    #     cls._delete_all_apps()
    #
    # @classmethod
    # def tearDownClass(cls):
    #     cls._delete_all_apps()
    #
    # @classmethod
    # def _delete_all_apps(cls):
    #     for app in cls.app_mng.lst():
    #         cls.app_mng.delete(str(app['id']))

    def _create_app(self, app_name):
        content = None
        try:
            content = self.app_mng.create(app_name)
        except LogsightException as err:
            print(f'Error creating app_name: {app_name} ({err.title})')

        self.assertIsInstance(content, dict)
        self.assertIsInstance(content['applicationId'], str)
        return content

    def _delete_app(self, app_id):
        content = self.app_mng.delete(app_id)
        self.assertIsInstance(content, dict)
        return content

    def test_lst_app(self):
        content = self.app_mng.lst()
        self.assertIsInstance(content, dict)
        self.assertTrue('applications' in content, dict)

    def test_create_delete_app(self):
        app_name = 'test_create_delete_app'
        content = self._create_app(app_name)
        self._delete_app(str(content['applicationId']))

    # def test_create_app_invalid_name(self):
    #     app_name = 'test-create-app'
    #     with self.assertRaises(BadRequest):
    #         self.app_mng.create(app_name)
    #
    # def test_create_duplicate(self):
    #     app_name = 'test_create_dup_app'
    #     content = self._create_app(app_name)
    #
    #     with self.assertRaises(BadRequest):
    #         self.app_mng.create(app_name)
    #
    #     self._delete_app(str(content['id']))
    #
    # def test_delete_no_app(self):
    #     app_id = '0123456789'
    #     with self.assertRaises(NotFound):
    #         self.app_mng.delete(app_id)
    #
    # def test_too_many_apps(self, n_apps=6):
    #     with self.assertRaises(BadRequest):
    #         self.test_create_list_delete_apps(n_apps)
    #     TestAppManagement._delete_all_apps()
    #
    # def test_create_list_delete_apps(self, n_apps=5):
    #     app_names = [f'test_create_app_{i}' for i in range(n_apps)]
    #     app_ids = [self._create_app(app_name)['id'] for app_name in app_names]
    #
    #     content = self.app_mng.lst()
    #     app_list = [(d['id'], d['name']) for d in content if 'test_create_app_' in d['name']]
    #
    #     self.assertCountEqual(zip(app_ids, app_names), app_list)
    #
    #     for _id in app_ids:
    #         self._delete_app(str(_id))

    # def test_list_with_invalid_key(self):
    #     private_key = '27x'
    #     with self.assertRaises(Unauthorized):
    #         LogsightApplication(private_key, EMAIL).lst()


if __name__ == '__main__':
    unittest.main()
