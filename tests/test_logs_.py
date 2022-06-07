import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_logs

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

    def test_send_logs_and_flush(self):
        n_log_messages = 60
        g = LogsightLogs(self.auth.token)
        p = generate_logs(n=n_log_messages)
        r1 = g.send(p, tags={'main': 'v1.1.3'}, app_id=self.app_id)
        print(r1)
        self.assertEqual(r1['logsCount'], n_log_messages)


if __name__ == '__main__':
    unittest.main()
