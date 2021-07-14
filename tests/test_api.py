import sys
import logging
import logging.handlers
import time
import unittest

from config import PRIVATE_KEY, APP_NAME
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now

NUMBER_LOG_BLOCKS_TO_SEND = 30
N_LOG_MESSAGES_TO_SEND = NUMBER_LOG_BLOCKS_TO_SEND * 15
DELAY_TO_QUERY_TEMPLATES = 30
DELAY_TO_QUERY_INCIDENTS = 90
DELAY_TO_QUERY_BACKEND = max(DELAY_TO_QUERY_INCIDENTS, DELAY_TO_QUERY_TEMPLATES)


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


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)

        logger, handler = cls.__setup_handler()

        for i in range(NUMBER_LOG_BLOCKS_TO_SEND):
            send_logs(logger, i)

        # Note: need to remove the handler before timing the end
        # Since the remove_handler will flush the messages in the internal buffer
        cls.__remove_handler(logger, handler)

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        print('Sleeping before querying backend', DELAY_TO_QUERY_BACKEND, 'sec')
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
        logger.addHandler(stdout_handler)
        return logger, handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_template_count(self):
        templates = LogsightResult(PRIVATE_KEY, APP_NAME).\
            get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_incident_count(self):
        incidents = LogsightResult(PRIVATE_KEY, APP_NAME).\
            get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertEqual(len(incidents), 1)


if __name__ == '__main__':
    unittest.main()
