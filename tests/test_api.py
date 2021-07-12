import unittest
import logging
from dateutil.tz import tzlocal
import datetime

from logsight.logger import LogsightLogger
from logsight.result import LogsightResult


class TestApi(unittest.TestCase):

    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    APP_NAME = 'unittest_11'

    @staticmethod
    def _start_time(start_time=None, minutes=60):
        # time format: = "%Y-%m-%dT%H:%M:%S.%f"
        if not start_time:
            start_time = datetime.datetime.now(tz=tzlocal()) - datetime.timedelta(minutes=minutes)
        return start_time.isoformat()

    @staticmethod
    def _end_time(end_time=None):
        # time format: = "%Y-%m-%dT%H:%M:%S.%f"
        if not end_time:
            end_time = datetime.datetime.now(tz=tz)
        return end_time.isoformat()

    @classmethod
    def setUpClass(cls):
        super(TestApi, cls).setUpClass()
        """ Load test data """

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(cls.PRIVATE_KEY, cls.APP_NAME)
        logsight_handler.setLevel(logging.DEBUG)
        logger.addHandler(logsight_handler)

        # for _ in range(1):
        #     logger.info("01. Hello World!")
        #     logger.error("02. Hello Error!")
        #     logger.warning("03. Hello Warning!")
        #     logger.debug("04. Hello Debug!")
        #     logger.info("05. Hello World!")
        #     logger.info("06. Hello World!")
        #     logger.info("07. Hello World!")
        #     logger.error("08. Hello Error!")
        #     logger.warning("09. Hello Warning!")
        #     logger.debug("10. Hello Debug!")
        #     logger.info("11. Hello World!")
        #     logger.info("12. Hello World!")

        cls.results = LogsightResult(cls.PRIVATE_KEY, cls.APP_NAME)

    def test_template_count(self):
        templates = self.results.get_results(self._start_time(), self._end_time(), 'parsing')
        self.assertEqual(len(templates), 12)

    def test_incident_count(self):
        incidents = self.results.get_results(self._start_time(), self._end_time(), 'incidents')
        self.assertEqual(len(incidents), 5)


if __name__ == '__main__':
    unittest.main()
