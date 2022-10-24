import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_singles

from logsight_sdk.config import set_host
from logsight_sdk.authentication import LogsightAuthentication
from logsight_sdk.logs import LogsightLogs

APP_NAME = 'unittest_TestLogs'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_singles(self):
        n_log_messages = 90
        g = LogsightLogs(self.auth.token)
        tags = {
            'system': 'hadoop',
            'version': '1.1.2',
            'env': 'pre-production'
        }
        p = generate_singles(tags, n=n_log_messages)
        res = g.send_singles(p)
        self.assertEqual(res['logsCount'], n_log_messages)


if __name__ == '__main__':
    unittest.main()
