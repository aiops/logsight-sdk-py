import unittest
import datetime
from dateutil.tz import tzlocal
import json

from tests.config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs, create_log_record
from logsight.incidents import LogsightIncident

from integration.send_logs import SendLogs

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

APP_NAME = 'class_test_incidents'


# "message":"starTime must be defined relative time in minutes (e.g., now, now-22m) or
# ISO timestamp YYYY-MM-DDTHH:mm:ss.SSSSSS+HH:00.
# If timezone is not specified, UTC is default

class TestIncidents(unittest.TestCase):

    app_id = None
    start_time = ''
    stop_time = ''

    @classmethod
    def setUpClass(cls):
        super(TestIncidents, cls).setUpClass()
        cls.u = LogsightUser(email=EMAIL, password=PASSWORD)
        print(cls.u)

        cls.app_mng = LogsightApplication(cls.u.user_id, cls.u.token)
        # cls.app_id = cls.app_mng.lst()['applications'][0]['applicationId']
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        print('app_id', cls.app_id)

        cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    @classmethod
    def _generate_logs(cls, delta=0, n=10):
        """ Generate logs using (a variation of) iso8106 format """
        m = "[main] org.apache.hadoop.mapreduce: Failed to connect. Executing with tokens: {i}"
        # '2021-03-23T01:02:51.007Z
        logs = [create_log_record(timestamp=(datetime.datetime.utcnow() + datetime.timedelta(days=delta))
                                  .strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                  level='INFO',
                                  message=m.format(i=i),
                                  metadata='') for i in range(max(n, 60))]
        return logs

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        logs = cls._generate_logs(delta=0, n=n_log_messages)
        cls.start_time, cls.stop_time = logs[0]['timestamp'], logs[-1]['timestamp']
        print(logs)

        g = LogsightLogs(cls.u.token)
        r = g.send(cls.app_id, logs, tag='v1.1.1')
        print(r)

        # cls.flush_id = g.flush(r1['receiptId'])['flushId']

    def test_incidents(self):
        i = LogsightIncident(self.u.user_id, self.u.token)
        now = datetime.datetime.utcnow()
        self.stop_time = now.isoformat()
        self.start_time = (now - datetime.timedelta(days=1)).isoformat()
        r = i.incidents(app_id=self.app_id, start_time=self.start_time, stop_time=self.stop_time, flush_id=None)
        self.assertEqual('data' in r, True)
        print(r)


if __name__ == '__main__':
    unittest.main()
