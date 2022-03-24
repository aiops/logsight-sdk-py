from logsight.config import HOST_API, PATH_LOGS_INCIDENTS
from logsight.api_client import APIClient


class LogsightIncident(APIClient):

    def __init__(self, user_id, token):
        """Class to manage applications (apps).

        Args:
            user_id (str): Identifier of the user.
            token (str): Access token.

        """
        super().__init__()
        self.user_id = user_id
        self.token = token

    def __str__(self):
        return f'user id = {self.user_id}, token = {self.token}'

    def incidents(self, app_id, start_time, stop_time,
                  flush_id=None, verbose=False):
        """Retrieves the incidents of logs.

        Args:
            app_id (str): Application id.
            start_time (str): Start time.
            stop_time (str): Stop time.
            flush_id (Union[str, None]): Flush id.
            verbose (bool): provides additional information.

        Returns:
            dict.
                {
                  "data": [
                    {
                      "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                      "semanticThreats": {},
                      "startTimestamp": "string",
                      "stopTimestamp": "string",
                      "totalScore": 0
                    }
                  ]
                }

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        payload = {
            'applicationId': app_id,
            'startTime': start_time,
            'stopTime': stop_time
        }
        if flush_id:
            payload.update({'flushId': flush_id})

        headers = {'content-type': 'application/json', 'Authorization': f'Bearer {self.token}'}
        return self._post(host=HOST_API,
                          path=PATH_LOGS_INCIDENTS.format(userId=self.user_id),
                          json=payload,
                          headers=headers,
                          verbose=verbose)
