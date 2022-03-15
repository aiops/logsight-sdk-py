import unittest
import datetime
import time

from tests.config import EMAIL, PASSWORD
from tests.utils import generate_logs
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.incidents import LogsightIncident
from logsight.exceptions import Conflict

APP_NAME = 'class_test_incidents'


class TestIncidents(unittest.TestCase):

    app_id = None
    start_time = ''
    stop_time = ''

    @classmethod
    def setUpClass(cls):
        super(TestIncidents, cls).setUpClass()
        cls.u = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.u.user_id, cls.u.token)
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
        g = LogsightLogs(cls.u.token)
        r = g.send(cls.app_id, logs, tag='v1.1.1')
        cls.flush_id = g.flush(r['receiptId'])['flushId']

    def test_incidents(self):
        i = LogsightIncident(self.u.user_id, self.u.token)
        now = datetime.datetime.utcnow()
        self.stop_time = now.isoformat()
        self.start_time = (now - datetime.timedelta(days=1)).isoformat()

        while True:
            try:
                r = i.incidents(app_id=self.app_id,
                                start_time=self.start_time,
                                stop_time=self.stop_time,
                                flush_id=self.flush_id)
                break
            except Conflict:
                time.sleep(10)

        self.assertEqual('data' in r, True)


if __name__ == '__main__':
    unittest.main()
