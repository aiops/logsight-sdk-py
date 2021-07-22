import requests
import urllib.parse
import html
import json

from logsight.exceptions import HTTP_EXCEPTION_MAP, DataCorruption
from logsight.template import Templates
from logsight.incidents import Incidents
from logsight.quality import LogQuality


ANOMALIES = {
    "log_ad": Templates,
    "incidents": Incidents,
    "log_quality": LogQuality,
}


class LogsightResult:

    host = 'https://logsight.ai'
    path = '/api_v1/results'

    def __init__(self, private_key, app_name):
        self.private_key = private_key
        self.app_name = app_name

    def get_results(self, start_time, end_time, anomaly_type):
        data = {'private-key': self.private_key,
                'app': self.app_name,
                'start-time': start_time,
                'end-time': end_time,
                'anomaly-type': anomaly_type}
        return self._build_object(anomaly_type, self._post(data=data))

    def _post(self, data):
        try:
            url = urllib.parse.urljoin(self.host, self.path)
            r = requests.post(url, json=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            # err = self._extract_elasticsearch_error(err)
            d = json.loads(err.response.text)
            description = d['description'] if 'description' in d else d
            raise HTTP_EXCEPTION_MAP[err.response.status_code](description)

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption('Content could not be converted from JSON: %s' % r.text)

    @staticmethod
    def _extract_elasticsearch_error(err):
        start_idx = err.response.text.find("<title>")
        end_idx = err.response.text.find("</title>")

        if start_idx != -1 and end_idx != -1:
            end_idx = end_idx + len("</title>")
            err = str(err) + ' (' + html.unescape(err.response.text[start_idx:end_idx]) + ')'

        return err

    def _build_object(self, anomaly_type, data):
        try:
            klass = ANOMALIES[anomaly_type.lower()]
        except KeyError as e:
            raise RuntimeError(f'No class found: {e}')
        except Exception as e:
            raise RuntimeError(f'Unknown error: {e}')

        return klass(data)
