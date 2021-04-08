from logging import StreamHandler
import requests

url = 'https://logsight.ai/api_v1/data'


class LogsightLogger(StreamHandler):

    def __init__(self, private_key, app_name):
        StreamHandler.__init__(self)
        self.private_key = private_key
        self.app_name = app_name

    def emit(self, record):
        msg = self.format(record)
        log_level = 'null'
        if self.level == 10:
            log_level = 'DEBUG'
        elif self.level == 20:
            log_level = 'INFO'
        elif self.level == 30:
            log_level = 'WARNING'
        elif self.level == 40:
            log_level = 'ERROR'
        elif self.level == 50:
            log_level = 'CRITICAL'
        myobj = {'private-key': self.private_key, 'app': self.app_name, 'message': msg, 'level': log_level}
        x = requests.post(url, json=myobj)
