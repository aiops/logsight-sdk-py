import requests
import urllib.parse
import json as js

from logsight.exceptions import from_dict, DataCorruption


class APIClient:

    def _get(self, host, path, params=None, headers=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.get(url, params=params or {}, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(js.loads(err.response.text))

        try:
            return js.loads(r.text)
        except js.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    def _post(self, host, path, json=None, files=None, headers=None,
              verbose=False):
        try:
            url = urllib.parse.urljoin(host, path)
            if json:
                r = requests.post(url, json=json, headers=headers)
            if files and not json:
                r = requests.post(url, files=files, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(js.loads(err.response.text))

        try:
            return js.loads(r.text)
        except js.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    def _delete(self, host, path, headers=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.delete(url, headers=headers)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise from_dict(js.loads(err.response.text))

        try:
            return js.loads(r.text)
        except js.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )
