import unittest
import random
import string

from tests.config import HOST_API, EMAIL, PASSWORD
from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 BadRequest,
                                 NotFound)


class TestApplications(unittest.TestCase):

    app_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestApplications, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplications(cls.auth.user_id, cls.auth.token)
        cls._delete_all_apps()

    @classmethod
    def tearDownClass(cls):
        cls._delete_all_apps()

    @classmethod
    def _delete_all_apps(cls):
        for app in cls.app_mng.lst()['applications']:
            cls.app_mng.delete(app['applicationId'])

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
        self._delete_app(content['applicationId'])

    def test_create_app_invalid_name(self):
        """applicationName must follow the following regex pattern ^[a-zA-Z0-9][a-zA-Z0-9_.-]+"""

        app_name = '-_test-create-app'
        with self.assertRaises(BadRequest):
            self.app_mng.create(app_name)

    def test_delete_inexistent_app_id(self):
        app_id = '3fa85f64-5717-4562-b3fc-2c963f66afa6'
        with self.assertRaises(NotFound):
            self.app_mng.delete(app_id)

    def test_delete_invalid_app_id(self):
        app_id = '0123456789'
        with self.assertRaises(BadRequest):
            self.app_mng.delete(app_id)

    # def test_create_too_many_apps(self, n_apps=6):
    #     with self.assertRaises(BadRequest):
    #         self.test_create_list_delete_apps(n_apps)
    #     TestAppManagement._delete_all_apps()

    def test_create_list_delete_apps(self, n_apps=5):
        app_names = [f'test_create_app_{i}' for i in range(n_apps)]
        app_ids = [self._create_app(app_name)['applicationId'] for app_name in app_names]

        content = self.app_mng.lst()['applications']
        app_list = [(d['applicationId'], d['name']) for d in content if 'test_create_app_' in d['name']]

        self.assertCountEqual(zip(app_ids, app_names), app_list)

        for _id in app_ids:
            self._delete_app(str(_id))

    def test_invalid_token(self):
        n = len(self.auth.token)
        token = 'a' * n
        while token == self.auth.token:
            token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=n))
        with self.assertRaises(Unauthorized):
            LogsightApplications(self.auth.user_id, token).lst()


if __name__ == '__main__':
    unittest.main()
