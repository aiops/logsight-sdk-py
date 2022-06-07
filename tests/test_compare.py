import time
import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_logs

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.compare import LogsightCompare
from logsight.exceptions import Conflict, InternalServerError
from logsight.logs import LogsightLogs

APP_NAME = 'unittest_compare_app'


class TestCompare(unittest.TestCase):
    app_id = None
    tag_v1 = {'version': 'v1.0.0'}
    tag_v2 = {'version': 'v2.0.0'}
    receipt_id = None

    @classmethod
    def setUpClass(cls):
        super(TestCompare, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplications(cls.auth.user_id, cls.auth.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        g = LogsightLogs(cls.auth.token)
        g.send(generate_logs(delta=0, n=n_log_messages), tags=cls.tag_v1, app_id=cls.app_id)
        r2 = g.send(generate_logs(delta=-2, n=n_log_messages), tags=cls.tag_v2, app_id=cls.app_id)
        cls.receipt_id = r2['receiptId']

    def test_compare(self):
        comp = LogsightCompare(self.auth.user_id, self.auth.token)
        max_attempts = 5
        attempt = 0
        r = None
        while attempt < max_attempts:
            try:
                r = comp.compare(baseline_tags=self.tag_v1,
                                 candidate_tags=self.tag_v2,
                                 log_receipt_id=self.receipt_id)
                break
            except Conflict:
                time.sleep(1)
                attempt += 1
            except InternalServerError:
                time.sleep(1)
                attempt += 1

        self.assertIsInstance(r, dict)
        self.assertTrue('totalLogCount' in r)


if __name__ == '__main__':
    unittest.main()
