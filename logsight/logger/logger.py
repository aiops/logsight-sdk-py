from logging.handlers import BufferingHandler
import time

from logsight.logs import LogsightLogs, create_log_record


class LogsightLogger(BufferingHandler):
    buffer_lifespan_seconds = 1

    def __init__(self, token, tags, app_name=None, app_id=None, metadata=None):
        """Creates an logger handler.

        Args:
            token (str): Token.
            app_name (str): Application name.
            app_id (str): Application id.
            tags (dict): Tags.
            metadata (str): Metadata.

        """
        BufferingHandler.__init__(self, capacity=128)
        self.logsight_logs = LogsightLogs(token)

        self.last_emit = 0
        self.token = token
        self.app_name = app_name
        self.app_id = app_id
        self.tags = tags
        self.metadata = metadata or ''

    def __str__(self):
        return f'app name = {self.app_name}, app id = {self.app_id}, token = {self.token}'

    def set_tags(self, tags):
        self.flush()
        self.tags = tags

    def set_metadata(self, metadata):
        self.metadata = metadata

    def flush(self):
        self.acquire()
        try:
            msgs = [create_log_record(record.levelname, self.format(record))
                    for record in self.buffer]
            if msgs:
                self.logsight_logs.send(log_lst=msgs, tags=self.tags, app_id=self.app_id, app_name=self.app_name)
            self.buffer = []
        finally:
            self.release()

    def emit(self, record):
        self.last_emit = time.time()
        super().emit(record)

    def shouldFlush(self, record):
        return (
            True
            if super().shouldFlush(record)
               or time.time() - self.last_emit > self.buffer_lifespan_seconds
            else False
        )
