from logging import StreamHandler
import datetime
import requests
import urllib.parse


class LogsightLogger(StreamHandler):

    host = 'https://logsight.ai'
    path = '/api_v1/data'

    def __init__(self, private_key, app_name):
        StreamHandler.__init__(self)
        self.private_key = private_key
        self.app_name = app_name

    def emit(self, record):
        msg = self.format(record)
        json = {"logMessages": [
            {'private-key': self.private_key,
             'app': self.app_name,
             'timestamp': datetime.datetime.now().isoformat(),
             'message': msg,
             'level': record.levelname}]
        }
        self._post(self.path, json=json)

    def _post(self, path, json):
        try:
            r = requests.post(urllib.parse.urljoin(self.host, path), json=json)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
