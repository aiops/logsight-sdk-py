from logging import StreamHandler
from logging.handlers import BufferingHandler
import time
import datetime
from dateutil.tz import tzlocal
import requests
import urllib.parse


class LogsightLogger(BufferingHandler):

    host = 'https://logsight.ai'
    path = '/api_v1/data'

    def __init__(self, private_key, app_name):
        BufferingHandler.__init__(self, capacity=128)
        self.last_emit = None
        # StreamHandler.__init__(self)
        self.private_key = private_key
        self.app_name = app_name

    def flush(self):
        self.acquire()
        try:
            messages = []
            for record in self.buffer:
                msg = self.format(record)
                messages.append(
                    {'private-key': self.private_key,
                     'app': self.app_name,
                     'timestamp': datetime.datetime.now(tz=tzlocal()).isoformat(),
                     'message': msg,
                     'level': record.levelname}
                )
            json = {"logMessages": messages}
            self._post(self.path, json=json)

            self.buffer = []
        finally:
            self.release()

    def emit(self, record):
        self.last_emit = time.time()
        super().emit(record)

    def shouldFlush(self, record):
        return True if super().shouldFlush(record) or time.time() - self.last_emit > 59 else False

    # def emit(self, record):
    #     msg = self.format(record)
    #     json = {"logMessages": [
    #         {'private-key': self.private_key,
    #          'app': self.app_name,
    #          'timestamp': datetime.datetime.now(tz=tzlocal()).isoformat(),
    #          'message': msg,
    #          'level': record.levelname}]
    #     }
    #     self._post(self.path, json=json)

    def _post(self, path, json):
        try:
            r = requests.post(urllib.parse.urljoin(self.host, path), json=json)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
