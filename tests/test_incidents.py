import unittest
import datetime
import time

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_logs

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.logs import LogsightLogs
from logsight.incidents import LogsightIncident
from logsight.exceptions import Conflict, InternalServerError

APP_NAME = 'class_test_incidents'


class TestIncidents(unittest.TestCase):

    app_id = None
    start_time = ''
    stop_time = ''

    @classmethod
    def setUpClass(cls):
        super(TestIncidents, cls).setUpClass()
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
        logs = generate_logs(delta=0, n=n_log_messages)
        cls.start_time, cls.stop_time = logs[0]['timestamp'], logs[-1]['timestamp']
        g = LogsightLogs(cls.auth.token)
        r = g.send(logs, tags={'version': 'v1.1.1'}, app_id=cls.app_id)
        cls.receipt_id = r['receiptId']

    def test_incidents(self):
        i = LogsightIncident(self.auth.user_id, self.auth.token)
        now = datetime.datetime.utcnow()
        self.stop_time = now.isoformat()
        self.start_time = (now - datetime.timedelta(days=1)).isoformat()

        max_attempts = 5
        attempt = 0
        r = None
        while attempt < max_attempts:
            try:
                r = i.incidents(app_id=self.app_id,
                                start_time=self.start_time,
                                stop_time=self.stop_time,
                                flush_id=self.receipt_id)
                break
            except Conflict:
                time.sleep(10)
                attempt += 1
            except InternalServerError:
                time.sleep(10)
                attempt += 1

        self.assertEqual('data' in r, True)


if __name__ == '__main__':
    unittest.main()
