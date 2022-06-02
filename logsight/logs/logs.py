import datetime

from dateutil.tz import tzlocal

from logsight.api_client import APIClient
from logsight.config import HOST_API
from logsight.config import PATH_LOGS


def create_log_record(level, message, timestamp=None, metadata=None):
    timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
    return {
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'metadata': metadata or '',
    }


class LogsightLogs(APIClient):

    def __init__(self, token):
        """Class to send log records.

        Args:
            token (str): Access token.

        """
        super().__init__()
        self.token = token

    def send(self, log_lst, tags, app_id=None, app_name=None):
        """Send log records to an application.

        Args:
            app_id (str): Application id.
            app_name (str): Application name.
            log_lst (List[dict]): Log records/messages.
                 [
                    {
                        'level': 'string',
                        'message': 'string',
                        'metadata': 'string',
                        'timestamp': 'string'
                    }
                ],
            tags (dict): Tags to associate with log records.

        Returns:
            dict:
            {
              "applicationId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "logsCount": 0,
              "receiptId": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
              "source": "string"
            }

        Raises:
            TODO(jcardoso)

        """
        if app_name is None and app_id is not None:
            payload = {
                'applicationId': app_id,
                'logs': log_lst,
                'tags': tags
            }
        elif app_name is not None and app_id is None:
            payload = {
                'applicationName': app_id,
                'logs': log_lst,
                'tags': tags
            }
        else:
            raise AttributeError("Please provide correct application name or ID")

        headers = {
            "content-type": "application/json",
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=HOST_API,
                          path=PATH_LOGS,
                          json=payload,
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
