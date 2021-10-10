from collections.abc import MutableSequence

from .quality import Quality


class SemanticAd(MutableSequence):
    def __init__(self, semantic_ad):
        if type(semantic_ad) is not list:
            raise ValueError()

        self._inner_list = semantic_ad

    def __len__(self):
        return len(self._inner_list)

    def __getitem__(self, index):
        return SemanticAd(self._inner_list.__getitem__(index))

    def __setitem__(self, key, value):
        self._inner_list[key] = value

    def __delitem__(self, key):
        del self._inner_list[key]

    def insert(self, key, value):
        self._inner_list.insert(key, value)


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
