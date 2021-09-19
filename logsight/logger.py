from logging.handlers import BufferingHandler
import time
import datetime
from dateutil.tz import tzlocal
import requests
import urllib.parse
import json

from logsight.config import HOST_API_V1, PATH_DATA
from logsight.exceptions import HTTP_EXCEPTION_MAP


class LogsightLogger(BufferingHandler):

    buffer_lifespan_seconds = 1

    def __init__(self, private_key, email, app_name):
        BufferingHandler.__init__(self, capacity=128)
        self.last_emit = None
        self.private_key = private_key
        self.email = email
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
            self._post(PATH_DATA, j)

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
            r = requests.post(urllib.parse.urljoin(HOST_API_V1, path), json=j)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            d = json.loads(err.response.text)
            description = d['description'] if 'description' in d else d
            raise HTTP_EXCEPTION_MAP[err.response.status_code](description)

        try:
            return r.status_code, json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print('Content could not be converted to JSON', r.text)
            return {}
