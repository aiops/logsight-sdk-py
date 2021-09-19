from collections.abc import MutableSequence


class Templates(MutableSequence):
    def __init__(self, templates):
        if type(templates) is not list:
            raise ValueError()

        self._inner_list = templates

    def __len__(self):
        return len(self._inner_list)

    def __getitem__(self, index):
        return Template(self._inner_list.__getitem__(index))

    def __setitem__(self, key, value):
        self._inner_list[key] = value

    def __delitem__(self, key):
        del self._inner_list[key]

    def insert(self, key, value):
        self._inner_list.insert(key, value)


class Template:
    """
    This class represents an Template.
    The reference can be found here https://docs.logsight.ai/en/rest/reference/objects#template

    Example of the structure returned
    {
       "@timestamp":"2021-07-11T07:27:55.478091",
       "actual_level":"WARNING",
       "app_name":"unittest_6",
       "message":"nova.virt.libvirt.imagecache [req-addc1839-2ed5-4778-b57e-5854eb7b8b09 - - - - -]",
       "name":"log",
       "param_0":"[req-addc1839-2ed5-4778-b57e-5854eb7b8b09",
       "param_1":"Unknown",
       "param_2":"file:",
       "param_3":"/var/lib/nova/instances/_base/a489c868f0c37da93b76227c91bb03908ac0e742",
       "template":"nova.virt.libvirt.imagecache <*> - - - - -] <*> base <*> <*>"
    }
    """

    def __init__(self, data):
        self._timestamp = data.get("@timestamp", None)
        self._actual_level = data.get("actual_level", None)
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
