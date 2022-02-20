import sys
import logging
from dateutil.tz import tzlocal
import datetime

from logsight.logger.logger import LogsightLogger
from logsight.utils import now, create_apps, delete_apps
from logsight.exceptions import LogsightException
from utils import p_sleep, SLEEP


if __name__ == '__main__':
    from load_logs import load_log_file, LOG_FILES
else:
    from .load_logs import load_log_file, LOG_FILES

LOGGING_TO_SYS_STDOUT = True


class SendLogs:

    def __init__(self, private_key, email, app_name):
        self.private_key = private_key
        self.email = email
        self.app_name = app_name
        self.logger, self.handler = self.__setup_handler(private_key, email, app_name)
        self.logger.propagate = False

        self.dt_start = '2021-10-07T13:18:09.178477+02:00'
        self.dt_end = datetime.datetime.now(tz=tzlocal()).isoformat()

    @staticmethod
    def __setup_handler(private_key, email, app_name):

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        logsight_handler = LogsightLogger(private_key, email, app_name)
        logsight_handler.setLevel(logging.DEBUG)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)

        logger.addHandler(logsight_handler)
        if LOGGING_TO_SYS_STDOUT:
            logger.addHandler(stdout_handler)

        return logger, logsight_handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    def create_app_name(self):
        try:
            delete_apps(self.private_key, self.email, [self.app_name])
        except LogsightException as e:
            print(e)

        try:
            create_apps(self.private_key, self.email, [self.app_name])
        except LogsightException as e:
            print(e)

    def delete_app_name(self):
        p_sleep(SLEEP.BEFORE_DELETE_APP)
        try:
            delete_apps(self.private_key, self.email, [self.app_name])
        except LogsightException as e:
            print(e)

    def send_log_messages(self, log_file_name, n_messages, tag=None, verbose=False):
        self.dt_start = now()
        print('Starting message sending', self.dt_start)

        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            if verbose and i % 100 == 0:
                print(f'Sending message # (app_name: {self.app_name}): {i}')
            self.send_log_message(i, level, message, tag)

        self.dt_end = now()
        print('Ended message sending', self.dt_end)

        return self.dt_start, self.dt_end

    def send_log_message(self, i, level, message, tag):

        self.handler.set_tag(tag)

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
