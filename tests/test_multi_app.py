import sys
import unittest
import logging
import time
from multiprocessing import Process
from ddt import ddt, data, unpack

from config import PRIVATE_KEY, DELAY_TO_QUERY_BACKEND
from integration.load_logs import LOG_FILES
from integration.send_logs import SendLogs
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now
from logsight.applications import LogsightApplication


N_LOG_MESSAGES_TO_SEND = 500
MAP_APP_NAME_LOG_FILE = [('hadoop', N_LOG_MESSAGES_TO_SEND, 'hadoop', 0),
                         ('openstack', N_LOG_MESSAGES_TO_SEND, 'openstack', 0),
                         ('mac', N_LOG_MESSAGES_TO_SEND, 'mac', 1),
                         ('zookeeper', N_LOG_MESSAGES_TO_SEND, 'zookeeper', 0),
                         ('openssh', N_LOG_MESSAGES_TO_SEND, 'openssh', 1),
                         ]


@ddt
class TestMultiApp(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestMultiApp, self).__init__(*args, **kwargs)

    @classmethod
    def setUpClass(cls):
        super(TestMultiApp, cls).setUpClass()

        cls.__create_apps()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)
        print('Sending n messages:', sum([n for _, n, _, _ in MAP_APP_NAME_LOG_FILE]))

        def run_cpu_tasks_in_parallel(tasks):
            running_tasks = [Process(target=args[0], args=(*args[1:],)) for args in tasks]
            for running_task in running_tasks:
                running_task.start()
            for running_task in running_tasks:
                running_task.join()

        def send_log_messages(log_file_id, n_log_messages_to_send, app_name, n_incidents):
            s = SendLogs(PRIVATE_KEY, app_name)
            s.send_log_messages(log_file_name=LOG_FILES[log_file_id], n_messages=n_log_messages_to_send)
            s.flush()

        run_cpu_tasks_in_parallel([(send_log_messages, *a) for a in MAP_APP_NAME_LOG_FILE])

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        print('Sleeping before querying backend:', DELAY_TO_QUERY_BACKEND, 'sec')
        time.sleep(DELAY_TO_QUERY_BACKEND)

    @staticmethod
    def __create_apps():
        app_mng = LogsightApplication(PRIVATE_KEY)

        for app_name in [i[2] for i in MAP_APP_NAME_LOG_FILE]:
            try:
                status_code, content = app_mng.create(app_name)
                print('Created app_name', app_name)
                if status_code != 200:
                    raise SystemExit('Error creating app', app_name)
            except SystemExit:
                print('app_name already exists', app_name)

    @data(*MAP_APP_NAME_LOG_FILE)
    @unpack
    def test_template_count(self, log_file, n_log_messages_to_send, app_name, n_incidents):
        templates = LogsightResult(PRIVATE_KEY, app_name).get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), n_log_messages_to_send)

    @data(*MAP_APP_NAME_LOG_FILE)
    @unpack
    def test_incident_count(self, log_file, n_log_messages_to_send, app_name, n_incidents):
        incidents = LogsightResult(PRIVATE_KEY, app_name)\
            .get_results(self.dt_start, self.dt_end, 'incidents')
        real_incidents = sum([1 if i.total_score > 0 else 0 for i in incidents])
        self.assertEqual(real_incidents, n_incidents)


if __name__ == '__main__':
    unittest.main()
