from collections.abc import MutableSequence


class LogQuality(MutableSequence):
    def __init__(self, templates):
        if type(templates) is not list:
            raise ValueError()

        self._inner_list = templates

    def __len__(self):
        return len(self._inner_list)

    def __getitem__(self, index):
        return Quality(self._inner_list.__getitem__(index))

    def __setitem__(self, key, value):
        self._inner_list[key] = value

    def __delitem__(self, key):
        del self._inner_list[key]

    def insert(self, key, value):
        self._inner_list.insert(key, value)


class Quality:
    """
    This class represents an Quality.
    The reference can be found here https://docs.logsight.ai/en/rest/reference/objects#quality

    Example of the structure returned
    {
        '@timestamp': '2021-07-19T18:39:23.238609',
        'actual_level': 'INFO',
        'app_name': 'unittest',
        'message': '0.1. Hello World!',
        'name': 'log',
        'param_0': '0.1.',
        'predicted_log_level': 'info',
        'prediction': 0,
        'template': '<*> Hello World!'
    }
    """

    def __init__(self, data):
        self._timestamp = data.get("@timestamp", None)
        self._actual_level = data.get("actual_level", None)
        self._predicted_log_level = data.get("predicted_log_level", None)
        self._app_name = data.get("app_name", None)
        self._message = data.get("message", None)
        self._name = data.get("name", None)
        self._params = data.get("params", None)
        self._template = data.get("template", None)

    def __repr__(self):
        return {"app_name": self._app_name, "template": self._template}

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def actual_level(self):
        return self._actual_level

    @property
    def predicted_log_level(self):
        return self._predicted_log_level

    @property
    def app_name(self):
        return self._app_name

    @property
    def message(self):
        return self._message

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params

    @property
    def template(self):
        return self._template
