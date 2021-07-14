import sys
import logging

from load_logs import load_log_file, LOG_FILES
from logsight.logger import LogsightLogger

PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
APP_NAME = 'unittest'


class SendLogs:

    def __init__(self, logger):
        self.logger = logger
        self.logger.propagate = False

    def send_log_messages(self, log_file_name, n_messages):
        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            print('Sending messsage', i)
            self.send_log_message(i, level, message)

    def send_log_message(self, i, level, message):
        if level.upper() == 'INFO':
            self.logger.info(message)
        elif level.upper() == 'WARNING':
            self.logger.warning(message)
        elif level.upper() == 'ERROR':
            self.logger.error(message)
        elif level.upper() == 'DEBUG':
            self.logger.debug(message)
        elif level.upper() == 'CRITICAL':
            self.logger.critical(message)
        else:
            sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))


if __name__ == '__main__':

    def setup_handler():
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.propagate = False

        handler = LogsightLogger(PRIVATE_KEY, APP_NAME)
        handler.setLevel(logging.DEBUG)
        logger.addHandler(handler)
        return logger, handler

    def remove_handler(logger, handler):
        logger.removeHandler(handler)

    logger, handler = setup_handler()
    r = SendLogs(logger)
    r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=200)
    remove_handler(logger, handler)
