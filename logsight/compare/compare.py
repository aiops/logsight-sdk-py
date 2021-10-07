from logsight.config import HOST_API
from logsight.config import PATH_COMPARE
from logsight.api_client import APIClient


class LogsightCompare(APIClient):

    def __init__(self, private_key, email, app_name):
        super().__init__()
        self.private_key = private_key
        self.email = email
        self.app_name = app_name

    def compare_time(self,
                     baseline_start_time, baseline_end_time,
                     test_start_time, test_end_time):
        data = {
            "private-key": self.private_key,
            "email": self.email,
            "app": self.app_name,
            "baseline": {
                "start-time": baseline_start_time,
                "end-time": baseline_end_time
            },
            "test": {
                "start-time": test_start_time,
                "end-time": test_end_time
            }
        }
        return self._get(HOST_API, PATH_COMPARE, data)

    def compare_tags(self, baseline_tag, test_tag):
        """Compare two log segments of an application using tags to identify
        the segments.

        Args:
            baseline_tag (str): Name of the baseline tag.
            test_tag (str): Name of the test tag.

        Returns:
            dict: ???.

        Raises:
            Unauthorized: If the private_key is invalid.
            Conflict: If the app_name already exists.

        """
        data = {
            "private-key": self.private_key,
            "email": self.email,
            "app": self.app_name,
            "baseline": {
                "tag": baseline_tag
            },
            "test": {
                "tag": test_tag
            }
        }
        return self._get(HOST_API, PATH_COMPARE, data)
