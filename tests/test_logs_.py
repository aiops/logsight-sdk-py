import unittest

# Comments for /logs endpoint
# - POST /api/v1/logs, a) the key 'logFormats' suggests the log messages may have several formats (plural)
#                      b) Adopt a general keyword for missing/unknown information, e.g., NONE
#                         e.g., "logFormats": "UNKNOWN_FORMAT" -> "NONE"
#

from tests.config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

APP_NAME = 'hello_app'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.user.user_id, cls.user.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']

    # @classmethod
    # def tearDownClass(cls):
    #     cls.app_mng.delete(cls.app_id)

    def _generate_logs(self, n=10):
        m = "2022-02-20 12:{minutes:02d}:48.963 INFO [main] org.apache.hadoop.mapreduce: Executing with tokens: {i}"
        return [m.format(minutes=i, i=i) for i in range(max(n, 60))]

    def test_logs(self):
        n_log_messages = 60
        g = LogsightLogs(self.user.token)
        r = g.send(self.app_id, self._generate_logs(n=n_log_messages), tag='v1.1.2')
        self.assertEqual(r['logsCount'], n_log_messages)

    # def test_invalid_app_id(self):
    #     n_log_messages = 60
    #     invalid_app_id = 'invalid_app_id'
    #     with self.assertRaises(BadRequest):
    #         LogsightLogs(self.user.token).send(invalid_app_id,
    #                                            self._generate_logs(n=n_log_messages),
    #                                            tag='v1.1.2')


if __name__ == '__main__':
    unittest.main()
