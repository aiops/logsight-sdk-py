import sys
import logging

from logsight.logger import LogsightLogger

if __name__ == '__main__':
    from load_logs import load_log_file, LOG_FILES
else:
    from .load_logs import load_log_file, LOG_FILES


class SendLogs:

    def __init__(self, private_key, app_name):
        self.private_key = private_key
        self.app_name = app_name
        self.logger, self.handler = self.__setup_handler(private_key, app_name)
        self.logger.propagate = False

    @staticmethod
    def __setup_handler(private_key, app_name):
        handler = LogsightLogger(private_key, app_name)
        handler.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(handler)

        return logger, handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    def send_log_messages(self, log_file_name, n_messages, app_name=None, verbose=False):
        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            if verbose and i % 100 == 0:
                print(f'Sending messsage # (app_name: {app_name}): {i}')
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

    def flush(self):
        self.__remove_handler(self.logger, self.handler)


if __name__ == '__main__':
    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    APP_NAME = 'unittest'

    r = SendLogs(APP_NAME)
    r.send_log_messages(log_file_name=LOG_FILES['hadoop'], n_messages=200)
    r.flush()
