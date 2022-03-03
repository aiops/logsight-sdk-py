import sys
import logging
import logging.handlers
import unittest
import datetime

from tests.config import EMAIL, PASSWORD
from logsight.application import LogsightApplication

from tests.integration.load_logs import LOG_FILES
from logsight.user import LogsightUser
from logsight.logger.logger import LogsightLogger

APP_NAME = 'test_logger'
N_LOG_MESSAGES_TO_SEND = 450
LOGGING_TO_SYS_STDOUT = True

if __name__ == '__main__':
    pass
else:
    from tests.integration.load_logs import load_log_file


def now():
    return datetime.datetime.utcnow().isoformat()


class TestLogger(unittest.TestCase):

    app_id = None
    user = None
    logger = None
    handler = None
    start_time = ''
    stop_time = ''

    @classmethod
    def setUpClass(cls):
        super(TestLogger, cls).setUpClass()
        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        print(cls.user)

        cls.app_mng = LogsightApplication(cls.user.user_id, cls.user.token)
        # cls.app_id = cls.app_mng.lst()['applications'][0]['applicationId']
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        print('app_id', cls.app_id)

        cls.logger, cls.handler = cls.__setup_handler()

    @classmethod
    def tearDownClass(cls):
        # cls.app_mng.delete(cls.app_id)

        # Note: need to remove the handler before timing the end
        # Since the remove_handler will flush the messages in the internal buffer
        cls.__remove_handler(cls.logger, cls.handler)

    def test_logging(self):
        for tag in ['v1.1.1', 'v2.2.2']:
            self._send_log_messages(log_file_name=LOG_FILES['helloworld'],
                                    n_messages=N_LOG_MESSAGES_TO_SEND,
                                    tag=tag)

    @classmethod
    def __setup_handler(cls):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(cls.user.token, cls.app_id, tag='v1.1.2')
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

    def _send_log_messages(self, log_file_name, n_messages, tag=None, verbose=False):
        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            if verbose and i % 100 == 0:
                print(f'Sending message # (app_name: {self.app_id}): {i}')
            self._send_log_message(i, level, message, tag)

    def _send_log_message(self, i, level, message, tag):
        if level.lower() not in ['info', 'warning', 'error', 'debug', 'critical']:
            sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))

        self.handler.set_tag(tag)
        eval('self.logger.' + level.lower() + f"({message})")

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
