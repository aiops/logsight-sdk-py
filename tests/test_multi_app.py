import sys
import unittest
import logging
import time
from multiprocessing import Process
from ddt import ddt, data, unpack

from config import PRIVATE_KEY
from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.result import LogsightResult
from logsight.utils import now, n_seconds_ago


def _optional_settings():
    logging.basicConfig(stream=sys.stderr)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


N_LOG_MESSAGES_TO_SEND = 500
MAP_APP_NAME_LOG_FILE = [('hadoop', N_LOG_MESSAGES_TO_SEND, 'hadoop', 1),
                         ('openstack', N_LOG_MESSAGES_TO_SEND, 'openstack', 0),
                         ('mac', N_LOG_MESSAGES_TO_SEND, 'mac', 0)]

DELAY_TO_QUERY_TEMPLATES = 30
DELAY_TO_QUERY_INCIDENTS = 90
DELAY_TO_QUERY_BACKEND = max(DELAY_TO_QUERY_TEMPLATES, DELAY_TO_QUERY_INCIDENTS)


@ddt
class TestMultiApp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMultiApp, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        super(TestMultiApp, cls).setUpClass()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)
        print('Sending n messages', sum([n for _, n, _, _ in MAP_APP_NAME_LOG_FILE]))

        def run_cpu_tasks_in_parallel(tasks):
            running_tasks = [Process(target=args[0], args=(*args[1:],)) for args in tasks]
            for running_task in running_tasks:
                running_task.start()
            for running_task in running_tasks:
                running_task.join()

        def send_log_messages(log_file_id, n_log_messages_to_send, app_name, n_incidents):
            r = SendLogs(PRIVATE_KEY, app_name)
            r.send_log_messages(log_file_name=LOG_FILES[log_file_id], n_messages=n_log_messages_to_send)

        run_cpu_tasks_in_parallel([(send_log_messages, *a) for a in MAP_APP_NAME_LOG_FILE])

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        print('Sleeping before querying backend', DELAY_TO_QUERY_BACKEND, 'sec')
        time.sleep(DELAY_TO_QUERY_BACKEND)

    @data(*MAP_APP_NAME_LOG_FILE)
    @unpack
    def test_template_count(self, log_file, n_log_messages_to_send, app_name, n_incidents):
        templates = LogsightResult(PRIVATE_KEY, app_name).get_results(self.dt_start, self.dt_end, 'log_ad')
        # templates = LogsightResult(PRIVATE_KEY, app_name).get_results(n_seconds_ago(93 * 60), now(), 'log_ad')
        self.assertEqual(len(templates), n_log_messages_to_send)

    @data(*MAP_APP_NAME_LOG_FILE)
    @unpack
    def test_incident_count(self, log_file, n_log_messages_to_send, app_name, n_incidents):
        incidents = LogsightResult(PRIVATE_KEY, app_name).get_results(self.dt_start, self.dt_end, 'incidents')
        # incidents = LogsightResult(PRIVATE_KEY, app_name).get_results(n_seconds_ago(93 * 60), now(), 'incidents')

        print(app_name, len(incidents))

        self.assertEqual(len(incidents), n_incidents)


if __name__ == '__main__':
    unittest.main()
