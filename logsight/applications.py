import requests
import urllib.parse
import html
import json

from logsight.config import HOST_API, PATH_APP_CREATE, PATH_APP_LST, PATH_APP_DELETE
from logsight.exceptions import HTTP_EXCEPTION_MAP


class LogsightApplication:

    def __init__(self, private_key, email):
        self.private_key = private_key
        self.email = email

    def create(self, app_name):
        data = {'key': self.private_key,
                'name': app_name}
        return self._post(PATH_APP_CREATE, data)

    def lst(self):
        payload = {}
        query = f'{self.private_key}'
        return self._get('/'.join([PATH_APP_LST, query]), payload)

    def delete(self, app_id):
        data = {}
        query = f'{app_id}?key={self.private_key}'
        return self._post('/'.join([PATH_APP_DELETE, query]), data)

    def _get(self, path, params=None):
        try:
            url = urllib.parse.urljoin(HOST_API, path)
            r = requests.get(url, params=params or {})
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            # err = self._extract_elasticsearch_error(err)
            d = json.loads(err.response.text)
            description = d['description'] if 'description' in d else d
            raise HTTP_EXCEPTION_MAP[err.response.status_code](description)

        return r.status_code, json.loads(r.text)

    def _post(self, path, data):
        try:
            url = urllib.parse.urljoin(HOST_API, path)
            r = requests.post(url, json=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            # err = self._extract_elasticsearch_error(err)
            d = json.loads(err.response.text)
            description = d['description'] if 'description' in d else d
            raise HTTP_EXCEPTION_MAP[err.response.status_code](description)

        return r.status_code, json.loads(r.text)

    @staticmethod
    def _extract_elasticsearch_error(err):
        start_idx = err.response.text.find("<title>")
        end_idx = err.response.text.find("</title>")

        if start_idx != -1 and end_idx != -1:
            end_idx = end_idx + len("</title>")
            err = str(err) + ' (' + html.unescape(err.response.text[start_idx:end_idx]) + ')'

        return err
