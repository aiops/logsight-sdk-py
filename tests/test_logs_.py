import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_singles

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.logs import LogsightLogs

APP_NAME = 'unittest_TestLogs'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplications(cls.auth.user_id, cls.auth.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    def test_singles(self):
        n_log_messages = 90
        g = LogsightLogs(self.auth.token)
        tags = {
            'system': 'hadoop',
            'version': '1.1.2',
            'env': 'pre-production'
        }
        p = generate_singles(self.app_id, tags, n=n_log_messages)
        res = g.send_singles(p)[0]
        print(res)
        self.assertEqual(res['logsCount'], n_log_messages)


if __name__ == '__main__':
    unittest.main()
