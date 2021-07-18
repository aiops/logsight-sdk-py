import sys
import unittest
import logging
import time

from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from config import PRIVATE_KEY, APP_NAME, DELAY_TO_QUERY_BACKEND
from logsight.utils import now


N_LOG_MESSAGES_TO_SEND = 1000


class TestSingleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSingleApp, cls).setUpClass()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)

        logger, handler = cls.__setup_handler()

        r = SendLogs(logger)
        r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=N_LOG_MESSAGES_TO_SEND)

        cls.__remove_handler(logger, handler)

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        print('Sleeping before querying backend:', DELAY_TO_QUERY_BACKEND, 'sec')
        time.sleep(DELAY_TO_QUERY_BACKEND)

    @staticmethod
    def __setup_handler():
        handler = LogsightLogger(PRIVATE_KEY, APP_NAME)
        handler.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        # logger.addHandler(stdout_handler)
        return logger, handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    def test_template_count(self):
        templates = LogsightResult(PRIVATE_KEY, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_pseudo_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertEqual(len(incidents), 1)

    def test_real_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'incidents')
        real_incidents = sum([1 if i.total_score > 0 else 0 for i in incidents])
        self.assertEqual(real_incidents, 1)


if __name__ == '__main__':
    unittest.main()
