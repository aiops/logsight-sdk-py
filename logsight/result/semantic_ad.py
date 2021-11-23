from .quality import Quality


class SemanticAd(Quality):

    def __init__(self, data):
        Quality.__init__(self, data)
        self._index = data.get("index", None)

    def __repr__(self):
        return {
            "app_name": self._app_name,
            "index": self._index,
        }

    @property
    def index(self):
        """int: Index of the log message."""
        return self._index
