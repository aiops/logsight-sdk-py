from logging.handlers import BufferingHandler
import time

from logsight.logs import LogsightLogs, create_single


class LogsightLogger(BufferingHandler):
    buffer_lifespan_seconds = 1

    def __init__(self, token, app_name):
        """Creates an logger handler.

        Args:
            token (str): Token.
            app_name (str): Application name.

        """
        BufferingHandler.__init__(self, capacity=128)

        self.token = token
        self.app_name = app_name

        self.logsight_logs = LogsightLogs(token)
        self.last_emit = 0
        self.metadata = None
        self.tags = None

    def __str__(self):
        return f'token = {self.token}'

    def set_tags(self, tags):
        """sets the tags for log messages.

        Args:
            tags (dict): Tags.

        """
        self.flush()
        self.tags = tags

    def set_metadata(self, metadata):
        """sets the metadata for log messages.

        Args:
            metadata (str): Metadata.

        """
        self.flush()
        self.metadata = metadata

    def flush(self):
        self.acquire()
        try:
            msgs = [create_single(app_name=self.app_name,
                                  level=record.levelname,
                                  message=self.format(record),
                                  tags=self.tags,
                                  timestamp=None,
                                  metadata=self.metadata)
                    for record in self.buffer]
            if msgs:
                self.logsight_logs.send_singles(msgs)

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
