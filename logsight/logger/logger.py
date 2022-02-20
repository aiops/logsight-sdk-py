from logging.handlers import BufferingHandler
import time
import datetime
from dateutil.tz import tzlocal

from logsight.config import HOST_API, PATH_LOGS
from logsight.api_client import APIClient


class LogsightLogger(BufferingHandler, APIClient):

    buffer_lifespan_seconds = 1

    def __init__(self, token, app_id, tag=None):
        """Deletes an existing  application.

        Args:
            private_key (str): Private key.
            email (str): E-mail.
            tag (str): Tag added to the log message dict.

        """
        BufferingHandler.__init__(self, capacity=128)
        self.last_emit = None
        self.token = token
        self.app_id = app_id
        self.tag = tag

    def set_tag(self, tag):
        self.tag = tag

    def flush(self):
        self.acquire()
        try:
            messages = []
            for record in self.buffer:
                msg = self.format(record)
                timestamp = datetime.datetime.now(tz=tzlocal()).isoformat()
                messages.append(
                    {
                        "timestamp": timestamp,
                        "message": msg,
                        "level": record.levelname,
                    }
                )
            self._post(host=HOST_API,
                       path=PATH_LOGS,
                       data={"applicationId": self.app_id,
                             "logFormats": self.app_id,
                             "tag": self.tag,
                             "logs": messages},
                       headers={'Authorization': f'Bearer {self.token}'})

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
