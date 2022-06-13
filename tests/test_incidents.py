import unittest

from tests.config import HOST_API, EMAIL, PASSWORD

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication

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
        # cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        pass
    # @classmethod
    # def _send_logs(cls):
    #     n_log_messages = 90
    #     g = LogsightLogs(cls.auth.token)
    #     tags = {
    #         'system': 'hadoop',
    #         'version': '1.1.2',
    #         'env': 'pre-production'
    #     }
    #     logs = generate_singles(cls.app_id, tags, n=n_log_messages)
    #     cls.start_time, cls.stop_time = logs[0]['timestamp'], logs[-1]['timestamp']
    #
    #     res = g.send_singles(logs)[0]
    #     cls.receipt_id = res['receiptId']

    # def test_incidents(self):
    #     i = LogsightIncident(self.auth.token)
    #     now = datetime.datetime.utcnow()
    #     self.stop_time = now.isoformat()
    #     self.start_time = (now - datetime.timedelta(days=1)).isoformat()
    #
    #     max_attempts = 5
    #     attempt = 0
    #     r = None
    #     while attempt < max_attempts:
    #         try:
    #             r = i.incidents(app_id=self.app_id,
    #                             start_time=self.start_time,
    #                             stop_time=self.stop_time,
    #                             flush_id=self.receipt_id)
    #             break
    #         except Conflict:
    #             time.sleep(10)
    #             attempt += 1
    #         except InternalServerError:
    #             time.sleep(10)
    #             attempt += 1
    #
    #     self.assertEqual('data' in r, True)


if __name__ == '__main__':
    unittest.main()
