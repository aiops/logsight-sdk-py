import logging
import logging.handlers
import sys
import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.integration.load_logs import LOG_FILES

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.logger.logger import LogsightLogger

APP_NAME = 'app_test_logger'
N_LOG_MESSAGES_TO_SEND = 450
LOGGING_TO_SYS_STDOUT = True

if __name__ == '__main__':
    pass
else:
    from tests.integration.load_logs import load_log_file


class TestLogger(unittest.TestCase):
    app_id = None
    user = None
    logger = None
    handler = None

    @classmethod
    def setUpClass(cls):
        super(TestLogger, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplications(cls.auth.user_id, cls.auth.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        cls.logger, cls.handler = cls.__setup_handler()

    @classmethod
    def tearDownClass(cls):
        # Note: need to remove the handler before timing the end
        # Since the remove_handler will flush the messages in the
        # internal buffer
        cls.__remove_handler(cls.logger, cls.handler)
        cls.app_mng.delete(cls.app_id)

    def test_logging(self):
        for tag in ['v1.1.1', 'v2.2.2']:
            self._send_log_messages(log_file_name=LOG_FILES['helloworld'],
                                    n_messages=N_LOG_MESSAGES_TO_SEND,
                                    tags={'version': tag})

    @classmethod
    def __setup_handler(cls):
        logsight_handler = LogsightLogger(token=cls.auth.token,
                                          app_name=APP_NAME)
        logsight_handler.setLevel(logging.DEBUG)

        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        logger.addHandler(logsight_handler)

        if LOGGING_TO_SYS_STDOUT:
            stdout_handler = logging.StreamHandler(sys.stdout)
            stdout_handler.setLevel(logging.INFO)
            logger.addHandler(stdout_handler)

        return logger, logsight_handler

    @staticmethod
    def __remove_handler(logger, handler):
        handler.close()
        logger.removeHandler(handler)

    def _send_log_messages(self, log_file_name, n_messages,
                           tags=None, verbose=False):
        self.handler.set_tags(tags)
        for i, (level, message) in enumerate(load_log_file(log_file_name, n_messages)):
            if verbose and i % 100 == 0:
                print(f'Sending message # (app_name: {self.app_id}): {i}')
            self._send_log_message(i, level, message)

    def _send_log_message(self, i, level, message):
        if level.lower() not in ['info', 'warning', 'error', 'debug', 'critical']:
            sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))
        eval('self.logger.' + level.lower() + f"(\'{message}\')")


if __name__ == '__main__':
    unittest.main()
