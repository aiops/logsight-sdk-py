from logging.handlers import BufferingHandler
import time

from logsight.logs import LogsightLogs, create_log_record


class LogsightLogger(BufferingHandler):

    buffer_lifespan_seconds = 1
    logsight_logs = None

    def __init__(self, token, app_id, tag, metadata=None):
        """Creates an logger handler.

        Args:
            token (str): Token.
            app_id (str): Application id.
            tag (str): Tag.
            metadata (str): Metadata.

        """
        BufferingHandler.__init__(self, capacity=128)
        self.logsight_logs = LogsightLogs(token)

        self.last_emit = None
        self.token = token
        self.app_id = app_id
        self.tag = tag
        self.metadata = metadata or ''

    def set_tag(self, tag):
        self.tag = tag

    def set_metadata(self, metadata):
        self.metadata = metadata

    def flush(self):
        self.acquire()
        try:
            msgs = [create_log_record(record.levelname, self.format(record))
                    for record in self.buffer]
            self.logsight_logs.send(self.app_id, msgs, tag=self.tag)
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
