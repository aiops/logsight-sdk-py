from logsight.config import HOST_API_V1, PATH_RESULTS
from logsight.api_client import APIClient
from logsight.result.template import Templates
from logsight.result.incidents import Incidents
from logsight.result.quality import LogQuality


ANOMALIES = {
    "log_ad": Templates,
    "incidents": Incidents,
    "log_quality": LogQuality,
}


class LogsightResult(APIClient):
    def __init__(self, private_key, email, app_name):
        super().__init__()
        self.private_key = private_key
        self.email = email
        self.app_name = app_name

    def get_results(self, start_time, end_time, anomaly_type):
        data = {
            "private-key": self.private_key,
            "email": self.email,
            "app": self.app_name,
            "start-time": start_time,
            "end-time": end_time,
            "anomaly-type": anomaly_type,
        }
        return self._build_object(anomaly_type, self._post(HOST_API_V1, PATH_RESULTS, data))

    def _build_object(self, anomaly_type, data):
        try:
            klass = ANOMALIES[anomaly_type.lower()]
        except KeyError as e:
            raise RuntimeError(f"No class found: {e}")
        except Exception as e:
            raise RuntimeError(f"Unknown error: {e}")

        return klass(data)
