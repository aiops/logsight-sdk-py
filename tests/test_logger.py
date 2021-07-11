import logging
import unittest

from logsight.logger import LogsightLogger


class TestLogger(unittest.TestCase):

    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    APP_NAME = 'unittest_9'

    def test_send_logs(self):

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(self.PRIVATE_KEY, self.APP_NAME)
        logsight_handler.setLevel(logging.DEBUG)
        logger.addHandler(logsight_handler)

        logger.info("01. Hello World!")
        logger.error("02. Hello Error!")
        logger.warning("03. Hello Warning!")
        logger.debug("04. Hello Debug!")
        logger.info("05. Hello World!")
        logger.info("06. Hello World!")
        logger.info("07. Hello World!")
        logger.error("08. Hello Error!")
        logger.warning("09. Hello Warning!")
        logger.debug("10. Hello Debug!")
        logger.info("11. Hello World!")
        logger.info("12. Hello World!")


if __name__ == '__main__':
    unittest.main()
