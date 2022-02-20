import requests
import urllib.parse
import json

from logsight.exceptions import from_dict, DataCorruption


class APIClient:

    def _get(self, host, path, params=None, headers=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.get(url, params=params or {}, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(json.loads(err.response.text))

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    def _post(self, host, path, data, headers=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.post(url, json=data, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(json.loads(err.response.text))

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    def _delete(self, host, path, headers=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.delete(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(json.loads(err.response.text))

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )