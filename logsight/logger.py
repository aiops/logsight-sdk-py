from logging.handlers import BufferingHandler
import time
import datetime
from dateutil.tz import tzlocal
import requests
import urllib.parse
import json


class LogsightLogger(BufferingHandler):

    buffer_lifespan_seconds = 1

    host = 'https://logsight.ai'
    path = '/api_v1/data'

    def __init__(self, private_key, app_name):
        BufferingHandler.__init__(self, capacity=128)
        self.last_emit = None
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
            j = {"log-messages": messages}
            self._post(self.path, j)

            self.buffer = []
        finally:
            self.release()

    def emit(self, record):
        self.last_emit = time.time()
        super().emit(record)

    def shouldFlush(self, record):
        return True if super().shouldFlush(record) or \
                       time.time() - self.last_emit > self.buffer_lifespan_seconds else False

    def _post(self, path, j):
        try:
            r = requests.post(urllib.parse.urljoin(self.host, path), json=j)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)

        try:
            return r.status_code, json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print('Content could not be converted to JSON', r.text)
            return {}
