import unittest
import datetime

from config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs, create_log_record
from logsight.compare import LogsightCompare

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

APP_NAME = 'unittest_compare_app'


class TestLogs(unittest.TestCase):

    app_id = None
    receipt_id_v1 = None
    tag_v1 = 'v1.0.0'
    tag_v2 = 'v2.0.0'

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
    def _generate_logs(cls, delta=0, n=10):
        """ Generate logs using (a variation of) iso8106 format """
        m = "[main] org.apache.hadoop.mapreduce: Executing with tokens: {i}"
        # '2021-03-23T01:02:51.007Z
        now = datetime.datetime.utcnow()
        d = now + datetime.timedelta(days=delta)
        logs = [create_log_record(timestamp=d.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
                                  level='INFO',
                                  message=m.format(i=i),
                                  metadata='') for i in range(max(n, 60))]
        return logs

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        g = LogsightLogs(cls.user.token)
        r1 = g.send(cls.app_id, cls._generate_logs(delta=0, n=n_log_messages), tag=cls.tag_v1)
        r2 = g.send(cls.app_id, cls._generate_logs(delta=-2, n=n_log_messages), tag=cls.tag_v2)
        print(r1)
        # cls.flush_id = g.flush(r1['receiptId'])['flushId']

    def test_compare(self):
        c = LogsightCompare(self.user.user_id, self.user.token)\
            .compare(app_id=self.app_id,
                     baseline_tag=self.tag_v1,
                     candidate_tag=self.tag_v2)
                     # flush_id=self.flush_id_v1)
        self.assertIsInstance(c, dict)
        self.assertTrue('totalLogCount' in c)

    # def test_tags(self):
    #     tags = LogsightCompare(self.user.user_id, self.user.token).tags(self.app_id)
    #     self.assertIsInstance(tags, list)
    #     self.assertEqual(len(tags), 2)


if __name__ == '__main__':
    unittest.main()
