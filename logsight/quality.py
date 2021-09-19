from collections.abc import MutableSequence

from .template import Template


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


class Quality(Template):
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
        Template.__init__(self, data)
        self._predicted_log_level = data.get("predicted_log_level", None)

    def __repr__(self):
        return {"app_name": self._app_name, "predicted_log_level": self._predicted_log_level}

    @property
    def predicted_log_level(self):
        return self._predicted_log_level
