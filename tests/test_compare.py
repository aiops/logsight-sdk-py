import unittest
import time

from tests.config import EMAIL, PASSWORD
from tests.utils import generate_logs
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare

from logsight.exceptions import Conflict

APP_NAME = 'unittest_compare_app'


class TestLogs(unittest.TestCase):

    app_id = None
    tag_v1 = 'v1.0.0'
    tag_v2 = 'v2.0.0'
    flush_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.user.user_id, cls.user.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        g = LogsightLogs(cls.user.token)
        g.send(cls.app_id, generate_logs(delta=0, n=n_log_messages), tag=cls.tag_v1)
        r2 = g.send(cls.app_id, generate_logs(delta=-2, n=n_log_messages), tag=cls.tag_v2)
        cls.flush_id = g.flush(r2['receiptId'])['flushId']

    def test_compare(self):
        comp = LogsightCompare(self.user.user_id, self.user.token)

        while True:
            try:
                r = comp.compare(app_id=self.app_id,
                                 baseline_tag=self.tag_v1,
                                 candidate_tag=self.tag_v2,
                                 flush_id=self.flush_id)
                break
            except Conflict:
                time.sleep(10)

        self.assertIsInstance(r, dict)
        self.assertTrue('totalLogCount' in r)


if __name__ == '__main__':
    unittest.main()
