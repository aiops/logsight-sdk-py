import datetime
from dateutil.tz import tzlocal

from logsight.config import HOST_API
from logsight.config import PATH_LOGS, PATH_LOGS_FLUSH
from logsight.api_client import APIClient


def create_log_record(level, message, timestamp=None, metadata=None):
    return {
        'timestamp': timestamp or datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        # 'timestamp': timestamp or datetime.datetime.now(tz=tzlocal()).isoformat(),
        'level': level,
        'message': message,
        'metadata': metadata or '',
    }


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
            log_lst (List[dict]): Log records/messages.
                 [
                    {
                        'level': 'string',
                        'message': 'string',
                        'metadata': 'string',
                        'timestamp': 'string'
                    }
                ],
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
        payload = {
            'applicationId': app_id,
            'logs': log_lst,
            'tag': tag
        }
        headers = {"content-type": "application/json", 'Authorization': f'Bearer {self.token}'}
        return self._post(host=HOST_API,
                          path=PATH_LOGS,
                          json=payload,
                          headers=headers)

    def flush(self, receipt_id):
        """Notify the server that the logs should be processed.

        Args:
            receipt_id (str): receipt id.

        Returns:
            dict:
                {
                  "flushId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "status": "DONE"
                }

        Raises:
            TODO(jcardoso)

        """
        payload = {
            'receiptId': receipt_id,
        }
        headers = {"content-type": "application/json", 'Authorization': f'Bearer {self.token}'}
        return self._post(host=HOST_API,
                          path=PATH_LOGS_FLUSH,
                          json=payload,
                          headers=headers)
