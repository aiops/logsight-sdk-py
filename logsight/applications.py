import requests
import urllib.parse
import html
import json

from logsight.template import Templates
from logsight.incidents import Incidents


ANOMALIES = {
    "log_ad": Templates,
    "incidents": Incidents,
    # "log_ad": LogAd,
    # "count_ad": CountAd,
}


class LogsightApplication:

    host = 'https://logsight.ai'
    path_create = '/api/applications/create'
    path_delete = '/api/applications'

    def __init__(self, private_key):
        self.private_key = private_key

    def create(self, app_name):
        data = {'key': self.private_key,
                'name': app_name}
        return self._post(data, self.path_create)

    def delete(self, app_id):
        data = {'key': self.private_key}
        p = '/'.join([self.path_delete, app_id])
        return self._post(data, p)

    def _post(self, data, path):
        try:
            url = urllib.parse.urljoin(self.host, path)
            r = requests.post(url, json=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            err = self._extract_elasticsearch_error(err)
            raise SystemExit(err)

        return json.loads(r.text)

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


if __name__ == '__main__':
    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    # PRIVATE_KEY = 'this.key'
    APP_NAME = 'unittest_4'

    app = LogsightApplication(PRIVATE_KEY)
    app_id = app.create(APP_NAME)
    print(app_id)
    result = app.delete(str(app_id['id']))
    print(result)
