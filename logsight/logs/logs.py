import json

from logsight.config import HOST_API
from logsight.config import PATH_LOGS
from logsight.api_client import APIClient


class LogsightLogs(APIClient):

    def __init__(self, token):
        """Class to manage applications (apps).

        Args:
            user_id (str): Identifier of the user.
            token (str): Access token.

        """
        super().__init__()
        self.token = token

    def send(self, app_id, log_lst, tag):
        """Creates a new application.

        Args:
            app_id (str): Application id.
            log_lst (List[str]): Log records/messages.
            tag (str): Tag to associate with log records.

        Returns:
            dict:
            {
              "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "logsCount": 0,
              "receiptId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "source": "string"
            }

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        payload = {'applicationId': app_id,
                   'logFormats': 'UNKNOWN_FORMAT',
                   'logs': log_lst,
                   'tag': tag
                   }
        headers = {"content-type": "application/json", 'Authorization': f'Bearer {self.token}'}
        return self._post(host=HOST_API,
                          path=PATH_LOGS,
                          json=payload,
                          headers=headers)
