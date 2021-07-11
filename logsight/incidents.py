from collections.abc import MutableSequence


class Incidents(MutableSequence):
    def __init__(self, incidents):
        if type(incidents) is not list:
            raise ValueError()

        self._inner_list = incidents

    def __len__(self):
        return len(self._inner_list)

    def __getitem__(self, index):
        return Incident(self._inner_list.__getitem__(index))

    def __setitem__(self, key, value):
        self._inner_list[key] = value

    def __delitem__(self, key):
        del self._inner_list[key]

    def insert(self, key, value):
        self._inner_list.insert(key, value)


class Incident:
    """
    This class represents an Incident.
    The reference can be found here https://docs.logsight.ai/en/rest/reference/objects#incident

    Example of the structure returned
    [
    {
      "@timestamp":"2021-07-11T09:30:19",
      "count_ads":[],
      "new_templates":[],
      "semantic_ad":[
         [
            {
               "@timestamp":"2021-07-11T11:29:28.105741",
               "actual_level":"INFO",
               "app_name":"unittest_8",
               "index":4,
               "message":"[main] org.apache.hadoop.mapreduce.v2.app.MRAppMaster: OutputCommitter set in config null",
               "name":"log",
               "param_0":"org.apache.hadoop.mapreduce.v2.app.MRAppMaster:",
               "prediction":1,
               "template":"[main] <*> OutputCommitter set in config null"
            }
         ],
         [
            {
               "@timestamp":"2021-07-11T11:29:32.934900",
               "actual_level":"INFO",
               "app_name":"unittest_8",
               "index":23,
               "message":"[main] org.apache.hadoop.mapreduce.v2.app.job.impl.JobImpl",
               "name":"log",
               "param_0":"org.apache.hadoop.mapreduce.v2.app.job.impl.JobImpl:",
               "param_1":"job_1445144423722_0020",
               "prediction":1,
               "template":"[main] <*> Not uberizing <*> because: not enabled; too many maps; too much input;"
            }
         ],
      ],
      "semantic_count_ads":[],
      "timestamp_end":"2021-07-11T11:30:08.661874",
      "timestamp_start":"2021-07-11T11:29:27.077735",
      "total_score":7
   }
   ]
    """
    def __init__(self, data):
        self._timestamp = data.get("@timestamp", None)
        self._count_ads = data.get("count_ads", None)
        self._new_templates = data.get("new_templates", None)
        self._semantic_ad = data.get("semantic_ad", None)
        self._semantic_count_ads = data.get("semantic_count_ads", None)
        self._timestamp_start = data.get("timestamp_start", None)
        self._timestamp_end = data.get("timestamp_end", None)
        self._total_score = data.get("total_score", None)

    def __repr__(self):
        return {"timestamp": self._timestamp}

    @property
    def timestamp(self):
        return self._timestamp

    @property
    def count_ads(self):
        return self._count_ads

    @property
    def new_templates(self):
        return self._new_templates

    @property
    def semantic_ad(self):
        return self._semantic_ad

    @property
    def semantic_count_ads(self):
        return self._semantic_count_ads

    @property
    def timestamp_start(self):
        return self._timestamp_start

    @property
    def timestamp_end(self):
        return self._timestamp_end

    @property
    def total_score(self):
        return self._total_score
