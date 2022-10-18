from collections.abc import MutableSequence


class ResultSeq(MutableSequence):
    def __init__(self, input_list, klass):
        if type(input_list) is not list:
            raise ValueError()

        self._inner_list = input_list
        self._klass = klass

    def __len__(self):
        return len(self._inner_list)

    def __getitem__(self, index):
        return self._klass(self._inner_list.__getitem__(index))

    def __setitem__(self, key, value):
        self._inner_list[key] = value

    def __delitem__(self, key):
        del self._inner_list[key]

    def insert(self, key, value):
        self._inner_list.insert(key, value)

    def get_klass(self):
        return self._klass
