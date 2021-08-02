import sys
import logging
import logging.handlers
import time
import unittest

from config import PRIVATE_KEY, DELAY_TO_QUERY_BACKEND
from logsight.exceptions import LogsightException, InternalServerError
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now, create_apps, delete_apps

APP_NAME = 'hello_app'
DELAY_TO_SEND_LOG_MESSAGES = 10
NUMBER_LOG_BLOCKS_TO_SEND = 30
N_LOG_MESSAGES_TO_SEND = NUMBER_LOG_BLOCKS_TO_SEND * 15
LOGGING_TO_SYS_STDOUT = True


def artificial_sleep(text, sleep_time):
    print(text, sleep_time, 'sec')
    time.sleep(sleep_time)


def send_logs(logger, i):
    logger.info(f"{i}.1. Hello World!")
    logger.debug(f"{i}.2. Hello Debug!")
    logger.info(f"{i}.3. Hello World!")
    logger.info(f"{i}.4. Hello World!")
    logger.info(f"{i}.5. Hello World!")
    logger.error(f"{i}.6. Hello Error!")
    logger.warning(f"{i}.7. Hello Warning!")
    logger.error(f"{i}.8. Hello Error!")
    logger.warning(f"{i}.9. Hello Warning!")
    logger.debug(f"{i}.10. Hello Debug!")
    logger.info(f"{i}.11. Hello World!")
    logger.info(f"{i}.12. Hello World!")
    logger.info(f"{i}.13. Hello World!")
    logger.info(f"{i}.14. Hello World!")
    logger.info(f"{i}.15. Hello World!")


class TestHelloApp(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestHelloApp, cls).setUpClass()

        logger, handler = cls.__setup_handler()

        try:
            delete_apps(PRIVATE_KEY, [APP_NAME])
        except LogsightException as e:
            print(e)

        try:
            create_apps(PRIVATE_KEY, [APP_NAME])
        except LogsightException as e:
            print(e)

        artificial_sleep('Sleeping before sending log messages:', DELAY_TO_SEND_LOG_MESSAGES)

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)
        logger.info('Starting message sending: %s' % cls.dt_start)

        for i in range(NUMBER_LOG_BLOCKS_TO_SEND):
            send_logs(logger, i)

        # Note: need to remove the handler before timing the end
        # Since the remove_handler will flush the messages in the internal buffer
        cls.__remove_handler(logger, handler)

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        artificial_sleep('Sleeping before querying backend:', DELAY_TO_QUERY_BACKEND)

    @classmethod
    def tearDownClass(cls):
        # delete_apps(PRIVATE_KEY, [APP_NAME])
        pass

    @staticmethod
    def __setup_handler():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        handler = LogsightLogger(PRIVATE_KEY, APP_NAME)
        handler.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.INFO)

        logger.addHandler(handler)
        if LOGGING_TO_SYS_STDOUT:
            logger.addHandler(stdout_handler)

        return logger, handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    # def test_invalid_key(self):
    #     private_key = '27x'
    #     with self.assertRaises(LogsightException):
    #         LogsightResult(private_key, APP_NAME).\
    #             get_results(self.dt_start, self.dt_end, 'log_ad')

    def test_template_count(self):
        templates = LogsightResult(PRIVATE_KEY, APP_NAME).\
            get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_template_empty_app(self):
        pass

    def test_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, APP_NAME).\
            get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertEqual(len(incidents), 1)

    def test_incident_empty_app(self):
        pass

    def test_log_quality(self):
        quality = LogsightResult(PRIVATE_KEY, APP_NAME).\
            get_results(self.dt_start, self.dt_end, 'log_quality')
        self.assertEqual(len(quality), 1)
        self.assertEqual(quality[0].actual_level.upper(),
                         quality[0].predicted_log_level.upper())

    def test_log_quality_empty_app(self):
        pass


if __name__ == '__main__':
    unittest.main()
