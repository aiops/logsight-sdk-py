import unittest
import logging
import time

from config import PRIVATE_KEY, APP_NAME
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now


def _optional_settings():
    logging.basicConfig()
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)


NUMBER_LOG_BLOCKS_TO_SEND = 1
N_LOG_MESSAGES_TO_SEND = NUMBER_LOG_BLOCKS_TO_SEND * 15
DELAY_TO_QUERY_TEMPLATES = 30
DELAY_TO_QUERY_INCIDENTS = 90


def send_logs(logger):
    logger.info("01. Hello World!")
    logger.debug("02. Hello Debug!")
    logger.info("03. Hello World!")
    logger.info("04. Hello World!")
    logger.info("05. Hello World!")
    logger.error("06. Hello Error!")
    logger.warning("07. Hello Warning!")
    logger.error("08. Hello Error!")
    logger.warning("09. Hello Warning!")
    logger.debug("10. Hello Debug!")
    logger.info("11. Hello World!")
    logger.info("12. Hello World!")
    logger.info("13. Hello World!")
    logger.info("14. Hello World!")
    logger.info("15. Hello World!")


class TestApi(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(PRIVATE_KEY, APP_NAME)
        logsight_handler.setLevel(logging.DEBUG)
        logger.addHandler(logsight_handler)

        cls.dt_start = now()
        print('Starting message sending', cls.dt_start)

        for _ in range(NUMBER_LOG_BLOCKS_TO_SEND):
            send_logs(logger)

        cls.dt_end = now()
        print('Ended message sending', cls.dt_end)

        cls.results = LogsightResult(PRIVATE_KEY, APP_NAME)

    def test_template_count(self):
        time.sleep(DELAY_TO_QUERY_TEMPLATES)
        templates = self.results.get_results(self.dt_start, self.dt_end, 'log_ad')
        self.assertEqual(len(templates), N_LOG_MESSAGES_TO_SEND)

    def test_incident_count(self):
        time.sleep(DELAY_TO_QUERY_INCIDENTS)
        incidents = self.results.get_results(self.dt_start, self.dt_end, 'incidents')
        self.assertEqual(len(incidents), 1)


if __name__ == '__main__':
    unittest.main()
