import requests
import urllib.parse
import html
import json


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
        data = {}
        query = f'{app_id}?key={self.private_key}'
        return self._post(data, '/'.join([self.path_delete, query]))

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


if __name__ == '__main__':
    PRIVATE_KEY = 'q1oukwa2hzsoxg4j7arvd6q67ik'
    APP_NAME = 'unittest_7'

    app = LogsightApplication(PRIVATE_KEY)
    app_id = app.create(APP_NAME)
    print(app_id)
    # result = app.delete(str(app_id['id']))
    # result = app.delete(str(152))
    # print(result)
