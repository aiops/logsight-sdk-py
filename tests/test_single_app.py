import sys
import unittest
import logging
import time

from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.result import LogsightResult
from config import PRIVATE_KEY, APP_NAME
from logsight.utils import now


def _optional_settings():
    logging.basicConfig(stream=sys.stderr)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


_optional_settings()

N_LOG_MESSAGES_TO_SEND = 500
DELAY_TO_QUERY_TEMPLATES = 30
DELAY_TO_QUERY_INCIDENTS = 90


class TestSingleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSingleApp, cls).setUpClass()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)

        r = SendLogs(PRIVATE_KEY, APP_NAME)
        r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=N_LOG_MESSAGES_TO_SEND)

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        cls.results = LogsightResult(PRIVATE_KEY, APP_NAME)

    def test_template_count(self):
        print('Sleeping before querying backend', DELAY_TO_QUERY_TEMPLATES, 'sec')
        time.sleep(DELAY_TO_QUERY_TEMPLATES)

        templates = self.results.get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_incident_count(self):
        print('Sleeping before querying backend', DELAY_TO_QUERY_INCIDENTS, 'sec')
        time.sleep(DELAY_TO_QUERY_INCIDENTS)

        incidents = self.results.get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertEqual(len(incidents), 3)


if __name__ == '__main__':
    unittest.main()
