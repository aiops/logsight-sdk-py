import unittest
import time
import datetime

from config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs, create_log_record
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

    # @classmethod
    # def tearDownClass(cls):
    #     cls.app_mng.delete(cls.app_id)

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
        g.send(cls.app_id, cls._generate_logs(delta=0, n=n_log_messages), tag=cls.tag_v1)
        r2 = g.send(cls.app_id, cls._generate_logs(delta=-2, n=n_log_messages), tag=cls.tag_v2)
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
        print(r)


if __name__ == '__main__':
    unittest.main()
