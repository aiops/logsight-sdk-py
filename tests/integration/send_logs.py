import sys
import logging

from .load_logs import load_log_file, LOG_FILES
from logsight.logger import LogsightLogger

logger = logging.getLogger(__name__)
# logger.propagate = False
logging.basicConfig(stream=sys.stderr)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
APP_NAME = 'unittest_7'


class SendLogs:

    def __init__(self, private_key, app_name):
        self.private_key = private_key
        self.app_name = app_name

    def send_log_messages(self, log_file_name, n_messages):
        handler = self.__setup_logger()

        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            self.send_log_message(logger, i, level, message)

        self.__remove_logger(handler)

    def send_log_message(self, logger, i, level, message):
        if level.upper() == 'INFO':
            logger.info(message)
        elif level.upper() == 'WARNING':
            logger.warning(message)
        elif level.upper() == 'ERROR':
            logger.error(message)
        elif level.upper() == 'DEBUG':
            logger.debug(message)
        elif level.upper() == 'CRITICAL':
            logger.critical(message)
        else:
            sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))

    def __setup_logger(self):
        handler = LogsightLogger(self.private_key, self.app_name)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return handler

    @staticmethod
    def __remove_logger(handler):
        logger.removeHandler(handler)


if __name__ == '__main__':
    r = SendLogs(PRIVATE_KEY, APP_NAME)
    r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=200)
