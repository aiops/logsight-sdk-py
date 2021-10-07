import requests
import urllib.parse
import json

from logsight.exceptions import from_dict, DataCorruption


class APIClient:

    def _get(self, host, path, params=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.get(url, params=params or {})
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(json.loads(err.response.text))

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    def _post(self, host, path, data):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.post(url, json=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(json.loads(err.response.text))

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )
