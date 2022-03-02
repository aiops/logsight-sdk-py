import unittest
import datetime
from dateutil.tz import tzlocal
import json

from tests.config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs, create_log_record

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

APP_NAME = 'class_testlogs'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.u = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.u.user_id, cls.u.token)
        # cls.app_id = cls.app_mng.lst()['applications'][0]['applicationId']
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        print('user_id', cls.u.user_id)
        print('token', cls.u.token)
        print('app_id', cls.app_id)

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    def _generate_logs(self, n=10):
        """ Generate logs using (a variation of) iso8106 format """
        m = "[main] org.apache.hadoop.mapreduce: Executing with tokens: {i}"
        # '2021-03-23T01:02:51.007Z
        logs = [create_log_record(timestamp=datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                  level='INFO',
                                  message=m.format(i=i),
                                  metadata='') for i in range(max(n, 60))]
        return logs

    def test_send_logs(self):
        n_log_messages = 60
        g = LogsightLogs(self.u.token)
        p = self._generate_logs(n=n_log_messages)
        r = g.send(self.app_id, p, tag='v1.1.2')
        self.assertEqual(r['logsCount'], n_log_messages)
        self.assertEqual(r['source'], 'REST_BATCH')

    def test_send_logs_and_flush(self):
        n_log_messages = 60
        g = LogsightLogs(self.u.token)
        p = self._generate_logs(n=n_log_messages)
        r1 = g.send(self.app_id, p, tag='v1.1.3')
        self.assertEqual(r1['logsCount'], n_log_messages)
        self.assertEqual(r1['source'], 'REST_BATCH')

        with self.assertRaises(NotFound):
            r2 = g.flush(r1['receiptId'])
            self.assertEqual(r1['receiptId'], r2['flushId'])


if __name__ == '__main__':
    unittest.main()
