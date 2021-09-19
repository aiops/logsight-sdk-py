import unittest

from config import PRIVATE_KEY, EMAIL
from utils import p_sleep, SLEEP
from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.result import LogsightResult
from logsight.utils import now, create_apps, delete_apps
from logsight.exceptions import LogsightException

APP_NAME = 'test_single_app'
DELAY_TO_SEND_LOG_MESSAGES = 10
N_LOG_MESSAGES_TO_SEND = 1000
DELAY_TO_DELETE_APP = 10


class TestSingleApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestSingleApp, cls).setUpClass()

        cls.__create_apps()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)

        s = SendLogs(PRIVATE_KEY, EMAIL, APP_NAME)
        s.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=N_LOG_MESSAGES_TO_SEND)
        s.flush()

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        p_sleep(SLEEP.BEFORE_QUERY_BACKEND)

    @staticmethod
    def __create_apps():
        try:
            delete_apps(PRIVATE_KEY, EMAIL, [APP_NAME])
        except LogsightException as e:
            print(e)

        try:
            create_apps(PRIVATE_KEY, EMAIL, [APP_NAME])
        except LogsightException as e:
            print(e)

        p_sleep(SLEEP.AFTER_CREATE_APP)

    @classmethod
    def tearDownClass(cls):
        p_sleep(SLEEP.BEFORE_DELETE_APP)
        delete_apps(PRIVATE_KEY, EMAIL, [APP_NAME])

    def test_template_count(self):
        templates = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_pseudo_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertGreaterEqual(len(incidents), 1)

    def test_real_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
            .get_results(self.dt_start, self.dt_end, 'incidents')
        real_incidents = sum([1 if i.total_score > 0 else 0 for i in incidents])
        self.assertGreaterEqual(real_incidents, 0)


if __name__ == '__main__':
    unittest.main()
