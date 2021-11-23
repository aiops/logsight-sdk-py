
class Incident:

    def __init__(self, data):
        """Class representing an incident.

        Note:
            Timestamps are represented in ISO format with timezone information.
            e.g, 2021-10-07T13:18:09.178477+02:00.

        """
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
        """str: timestamp when the log message was generated."""
        return self._timestamp

    @property
    def count_ads(self):
        """:obj:`list` of :obj:`str`: Count ad."""
        return self._count_ads

    @property
    def new_templates(self):
        """:obj:`list` of :obj:`str`: list of new templates."""
        return self._new_templates

    @property
    def semantic_ad(self):
        """:obj:`list` of :obj:`SemanticAd`: semantic ad."""
        return self._semantic_ad

    @property
    def semantic_count_ads(self):
        """:obj:`list` of :obj:`str`: Semantic count ads."""
        return self._semantic_count_ads

    @property
    def timestamp_start(self):
        """str: Timestamp of the start of the incident."""
        return self._timestamp_start

    @property
    def timestamp_end(self):
        """str: Timestamp of end of the incident."""
        return self._timestamp_end

    @property
    def total_score(self):
        """str: Total score of the incident."""
        return self._total_score
