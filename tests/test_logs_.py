import unittest

from tests.config import EMAIL, PASSWORD
from tests.utils import generate_logs
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs

APP_NAME = 'class_testlogs'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.u = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.u.user_id, cls.u.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    def test_send_logs_and_flush(self):
        n_log_messages = 60
        g = LogsightLogs(self.u.token)
        p = generate_logs(n=n_log_messages)
        r1 = g.send(self.app_id, p, tag='v1.1.3')
        self.assertEqual(r1['logsCount'], n_log_messages)
        self.assertEqual(r1['source'], 'REST_BATCH')

        r = g.flush(r1['receiptId'])
        self.assertEqual(r['status'], 'PENDING')


if __name__ == '__main__':
    unittest.main()
