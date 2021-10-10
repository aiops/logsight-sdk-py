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

    def __init__(self, data):
        Template.__init__(self, data)
        self._predicted_log_level = data.get("predicted_log_level", None)
        self._prediction = data.get("prediction", None)

    def __repr__(self):
        return {
            "app_name": self._app_name,
            "predicted_log_level": self._predicted_log_level,
        }

    @property
    def predicted_log_level(self):
        """str: Predicted log level for the log message (e.g., WARNING)."""
        return self._predicted_log_level

    @property
    def prediction(self):
        """int: Prediction for the log message.
            1 (one) for INFO, DEBUG, TRACE.
            0 (zero) for WARNING, WARN, ERROR, EXCEPTION, CRITICAL.
        """
        return self._predicted_log_level
