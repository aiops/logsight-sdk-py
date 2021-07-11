import sys
import unittest
import logging
import datetime

from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.result import LogsightResult


logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


class TestApi(unittest.TestCase):

    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    APP_NAME = 'unittest_8'

    N_LOG_MESSAGES_TO_SEND = 300

    @staticmethod
    def _start_time(start_time=None, minutes=60):
        # time format: = "%Y-%m-%dT%H:%M:%S.%f"
        if not start_time:
            start_time = datetime.datetime.now() - datetime.timedelta(minutes=minutes)
        return start_time.isoformat()

    @staticmethod
    def _end_time(end_time=None):
        # time format: = "%Y-%m-%dT%H:%M:%S.%f"
        if not end_time:
            end_time = datetime.datetime.now()
        return end_time.isoformat()

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        """ Load test data """

        # generate random app_name
        # create new app_name using API

        # r = SendLogs(cls.PRIVATE_KEY, cls.APP_NAME)
        # SendLogs("q1oukwa2hzsoxg4j7arvd6q67ik", "unittest_8")
        # r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=cls.N_LOG_MESSAGES_TO_SEND)

        cls.results = LogsightResult(cls.PRIVATE_KEY, cls.APP_NAME)

    def test_template_count(self):
        templates = self.results.get_results(self._start_time(), self._end_time(), 'parsing')
        self.assertEqual(len(templates), self.N_LOG_MESSAGES_TO_SEND)

    def test_incident_count(self):
        incidents = self.results.get_results(self._start_time(), self._end_time(), 'incidents')
        self.assertEqual(len(incidents), 5)


if __name__ == '__main__':
    unittest.main()
