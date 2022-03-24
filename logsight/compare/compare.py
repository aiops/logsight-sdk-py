from logsight.config import HOST_API
from logsight.config import PATH_COMPARE, PATH_COMPARE_TAGS
from logsight.api_client import APIClient


class LogsightCompare(APIClient):

    def __init__(self, user_id, token):
        """Class to compare logs.

        Args:
            user_id (str): Identifier of the user.
            token (str): Access token.

        """
        super().__init__()
        self.user_id = user_id
        self.token = token

    def __str__(self):
        return f'user id = {self.user_id}, token = {self.token}'

    def compare(self, app_id, baseline_tag, candidate_tag,
                flush_id=None, verbose=False):
        """Compares the logs on an application.

        Args:
            app_id (str): Application id.
            baseline_tag (str): Tag of the baseline logs.
            candidate_tag (str): Tag of the candidate logs.

        Returns:
            dict.
                {
                  "addedStatesFaultPercentage": 0,
                  "addedStatesReportPercentage": 0,
                  "addedStatesTotalCount": 0,
                  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "baselineLogCount": 0,
                  "candidateChangePercentage": 0,
                  "candidateLogCount": 0,
                  "deletedStatesFaultPercentage": 0,
                  "deletedStatesReportPercentage": 0,
                  "deletedStatesTotalCount": 0,
                  "flushId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "frequencyChangeFaultPercentage": {},
                  "frequencyChangeReportPercentage": {},
                  "frequencyChangeTotalCount": 0,
                  "link": "string",
                  "recurringStatesFaultPercentage": 0,
                  "recurringStatesReportPercentage": 0,
                  "recurringStatesTotalCount": 0,
                  "risk": 0,
                  "totalLogCount": 0
                }

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        payload = {'applicationId': app_id,
                   'baselineTag': baseline_tag,
                   'candidateTag': candidate_tag,
                   'flushId': flush_id}
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=HOST_API,
                          path=PATH_COMPARE,
                          json=payload,
                          headers=headers,
                          verbose=verbose)

    def tags(self, app_id):
        """Lists of the tags of an application.

        Returns:
            List:
                [
                  {
                    "tag": "string",
                    "tagView": "string"
                  }
                ]

        Raises:
            Unauthorized: If the private_key is invalid.

        """
        params = {'applicationId': app_id, 'userId': self.user_id}
        headers = {'Authorization': f'Bearer {self.token}'}
        return self._get(host=HOST_API,
                         path=PATH_COMPARE_TAGS,
                         params=params,
                         headers=headers)
