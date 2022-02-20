import sys
import logging
import logging.handlers
import unittest
from dateutil.tz import tzlocal
import datetime

from utils import SLEEP, p_sleep
from config import EMAIL, USER_ID, PASSWORD
from tests.integration.send_logs import SendLogs
from tests.integration.load_logs import LOG_FILES
from logsight.user import LogsightUser
from logsight.logger.logger import LogsightLogger

APP_NAME = 'hello_app'
N_LOG_MESSAGES_TO_SEND = 450
LOGGING_TO_SYS_STDOUT = True


class TestLogger(unittest.TestCase):

    s = None

    @classmethod
    def setUpClass(cls):
        super(TestLogger, cls).setUpClass()

        cls.dt_start = '2021-10-07T13:18:09.178477+02:00'
        cls.dt_end = datetime.datetime.now(tz=tzlocal()).isoformat()

        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.s = SendLogs(cls.user.token, cls.user)

        cls.s.create_app_name()

        p_sleep(SLEEP.AFTER_CREATE_APP)

        cls.s.send_log_messages(log_file_name=LOG_FILES['helloworld'],
                                n_messages=N_LOG_MESSAGES_TO_SEND,
                                tag='v1')
        cls.dt_start = cls.s.dt_start
        cls.s.send_log_messages(log_file_name=LOG_FILES['helloworld'],
                                n_messages=N_LOG_MESSAGES_TO_SEND,
                                tag='v2')

        # Note: need to remove the handler before timing the end
        # Since the remove_handler will flush the messages in the internal buffer
        cls.s.flush()
        cls.dt_end = cls.s.dt_end

        p_sleep(SLEEP.BEFORE_QUERY_BACKEND)


    @classmethod
    def tearDownClass(cls):
        p_sleep(SLEEP.BEFORE_DELETE_APP)
        cls.s.delete_app_name()

    @staticmethod
    def __setup_handler():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(token, app_id, tag)
        logsight_handler.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)

        logger.addHandler(logsight_handler)
        if LOGGING_TO_SYS_STDOUT:
            logger.addHandler(stdout_handler)

        return logger, logsight_handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    # def test_template_count(self):
    #     templates = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME).\
    #         get_results(self.dt_start, self.dt_end, 'log_ad')
    #     self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)
    #
    # def test_incident_count(self):
    #     incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME).\
    #         get_results(self.dt_start, self.dt_end, 'incidents')
    #     self.assertIn(len(incidents), [1, 2])
    #
    # def test_log_quality(self):
    #     quality = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME).\
    #         get_results(self.dt_start, self.dt_end, 'log_quality')
    #     self.assertEqual(len(quality), 4)
    #     self.assertIn(quality[0].actual_level.upper(),
    #                   quality[0].predicted_level.replace(',', ' ').strip().split())
    #
    # def test_invalid_key(self):
    #     private_key = '27x'
    #     with self.assertRaises(Unauthorized):
    #         LogsightResult(private_key, EMAIL, APP_NAME).\
    #             get_results(self.dt_start, self.dt_end, 'log_ad')
    #
    # def test_invalid_app_name(self):
    #     invalid_app_name = 'invalid_app_name'
    #     with self.assertRaises(Unauthorized):
    #         LogsightResult(PRIVATE_KEY, EMAIL, invalid_app_name).\
    #             get_results(self.dt_start, self.dt_end, 'log_quality')
    #
    # def test_invalid_timestamp(self):
    #     timestamp_short = '2021-10-07'
    #     with self.assertRaises(BadRequest):
    #         LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME).\
    #             get_results(self.dt_start, timestamp_short, 'log_quality')
    #
    # def test_invalid_incident_type(self):
    #     with self.assertRaises(BadRequest):
    #         LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME).\
    #             get_results(self.dt_start, self.dt_end, 'invalid_incident_type')


if __name__ == '__main__':
    unittest.main()
