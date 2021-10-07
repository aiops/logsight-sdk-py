import requests
import urllib.parse
import json
import html

from logsight.exceptions import HTTP_EXCEPTION_MAP, DataCorruption


class APIClient:
    def __init__(self):
        pass

    def _get(self, host, path, params=None):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.get(url, params=params or {})
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            d = json.loads(err.response.text)
            description = d["description"] if "description" in d else d
            raise HTTP_EXCEPTION_MAP[err.response.status_code](description)

        try:
            return r.status_code, json.loads(r.text)
        except json.decoder.JSONDecodeError:
            print("Content could not be converted to JSON", r.text)
            return {}

    def _post(self, host, path, data):
        try:
            url = urllib.parse.urljoin(host, path)
            r = requests.post(url, json=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as err:
            try:
                d = json.loads(err.response.text)
                description = d["description"] if "description" in d else d
                raise HTTP_EXCEPTION_MAP[err.response.status_code](description)
            except json.decoder.JSONDecodeError:
                msg = self._extract_elasticsearch_error(err)
                raise HTTP_EXCEPTION_MAP[err.response.status_code](msg)

        try:
            return json.loads(r.text)
        except json.decoder.JSONDecodeError:
            raise DataCorruption(
                "Content could not be converted from JSON: %s" % r.text
            )

    @staticmethod
    def _extract_elasticsearch_error(err):
        start_idx = err.response.text.find("<title>")
        end_idx = err.response.text.find("</title>")

        if start_idx != -1 and end_idx != -1:
            end_idx = end_idx + len("</title>")
            err = (
                str(err)
                + " ("
                + html.unescape(err.response.text[start_idx:end_idx])
                + ")"
            )

        return err
