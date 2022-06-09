import datetime
from dateutil.tz import tzlocal

import logsight.config
from logsight.api_client import APIClient
from logsight.endpoints import PATH_LOGS_SINGLES


def create_single(app_id, level, message, tags, timestamp=None, metadata=None):
    timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
    r = {
        'applicationId': app_id,
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'tags': tags
    }
    if metadata:
        r.update({'metadata': metadata})
    return r


class LogsightLogs(APIClient):

    def __init__(self, token):
        """Class to send log records.

        Args:
            token (str): Access token.

        """
        super().__init__()
        self.token = token

    def send_singles(self, log_lst):
        """Send log records to an application.

        Args:
            log_lst (List[dict]): Log records/messages.
            [
              {
                "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                "applicationName": "string",
                "level": "string",
                "message": "string",
                "metadata": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "tags": {
                  "additionalProp1": "string",
                  "additionalProp2": "string",
                  "additionalProp3": "string"
                },
                "timestamp": "string"
              }
            ]

        Returns:
            list:
            [
                {
                  "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  "logsCount": 0,
                  "receiptId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                }
            ]

        """
        headers = {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        return self._post(host=logsight.config.HOST_API,
                          path=PATH_LOGS_SINGLES,
                          json=log_lst,
                          headers=headers)

    # def upload(self, app_id, file, tag):
    #     # Depricated in v1.1.0
    #     """Creates a new application.
    #
    #     Args:
    #         app_id (str): Application id.
    #         file (str): Log file
    #         tag (str): Tag to associate with log records.
    #
    #     Returns:
    #         dict:
    #         {
    #           "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #           "logsCount": 0,
    #           "receiptId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #           "source": "string"
    #         }
    #
    #     Raises:
    #         TODO(jcardoso)
    #
    #     """
    #     with open(file, 'rb') as f:
    #         files = {'file': (os.path.basename(file), f, 'text/csv')}
    #         headers = {'Authorization': f'Bearer {self.token}'}
    #         path = PATH_LOGS_FILE.format(applicationId=app_id, tag=tag)
    #         return self._post(host=HOST_API,
    #                           path=path,
    #                           files=files,
    #                           headers=headers)

    # Depricated in v1.1.0
    # def flush(self, receipt_id):
    #     """Notify the server that the logs should be processed.
    #
    #     Args:
    #         receipt_id (str): receipt id.
    #
    #     Returns:
    #         dict:
    #             {
    #               "flushId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
    #               "status": "DONE"
    #             }
    #
    #     Raises:
    #         TODO(jcardoso)
    #
    #     """
    #     payload = {
    #         'receiptId': receipt_id,
    #     }
    #     headers = {
    #         'content-type': 'application/json',
    #         'Authorization': f'Bearer {self.token}'
    #     }
    #     return self._post(host=HOST_API,
    #                       path=PATH_LOGS_FLUSH,
    #                       json=payload,
    #                       headers=headers)
