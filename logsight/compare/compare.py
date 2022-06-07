import logsight.config
from logsight.endpoints import (PATH_POST_COMPARE,
                                PATH_GET_COMPARE,
                                PATH_GET_COMPARE_ID,
                                PATH_DELETE_COMPARE,
                                PATH_POST_STATUS)
from logsight.api_client import APIClient


class LogsightCompare(APIClient):

    def __init__(self, token):
        """Class to compare logs.

        Args:
            token (str): Access token.

        """
        super().__init__()
        self.token = token

    def __str__(self):
        return f'token = {self.token}'

    def compare(self, baseline_tags, candidate_tags, log_receipt_id=None):
        """Compares the logs on an application.

        Args:
            baseline_tags (dict): Tags of the baseline logs.
            candidate_tags (dict): Tags of the candidate logs.

        Returns:
            dict.
                {
                  "addedStatesFaultPercentage": 0,
                  "addedStatesReportPercentage": 0,
                  "addedStatesTotalCount": 0,
                  "baselineLogCount": 0,
                  "baselineTags": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                  },
                  "candidateChangePercentage": 0,
                  "candidateLogCount": 0,
                  "candidateTags": {
                    "additionalProp1": "string",
                    "additionalProp2": "string",
                    "additionalProp3": "string"
                  },
                  "compareId": "string",
                  "deletedStatesFaultPercentage": 0,
                  "deletedStatesReportPercentage": 0,
                  "deletedStatesTotalCount": 0,
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
        payload = {
            'baselineTags': baseline_tags,
            'candidateTags': candidate_tags,
            'logsReceiptId': log_receipt_id
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=logsight.config.HOST_API,
                          path=PATH_POST_COMPARE,
                          json=payload,
                          headers=headers)

    def ls_comparisons(self):
        """List comparisons stored.

        Returns:
            dict.
                {
                  "listCompare": [
                    {
                      "_id": "string",
                      "_source": {
                        "baseline_tags": {
                          "additionalProp1": "string",
                          "additionalProp2": "string",
                          "additionalProp3": "string"
                        },
                        "candidate_tags": {
                          "additionalProp1": "string",
                          "additionalProp2": "string",
                          "additionalProp3": "string"
                        },
                        "risk": 0,
                        "severity": 0,
                        "status": 0,
                        "timestamp": "string"
                      }
                    }
                  ]
                }

        """
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._get(host=logsight.config.HOST_API,
                         path=PATH_GET_COMPARE,
                         headers=headers)

    def get_comparison_id(self, comp_id):
        """Get comparison with id comp_id.

        Args:
            comp_id (string): Comparison Id.

        Returns:
            dict.
                 {
                  "listCompare": [
                    {
                      "_id": "string",
                      "_source": {}
                    }
                  ]
                }

        """
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._get(host=logsight.config.HOST_API,
                         path=PATH_GET_COMPARE_ID.format(compareId=comp_id),
                         headers=headers)

    def rm_comparison_id(self, comp_id):
        """Remove comparison with id comp_id.

        Args:
            comp_id (string): Comparison Id.

        Returns:
            dict.
                {
                  "compareId": "string"
                }

        """
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._delete(host=logsight.config.HOST_API,
                            path=PATH_DELETE_COMPARE.format(compareId=comp_id),
                            headers=headers,
                            ignore_return_data=True)

    def set_status(self, comp_id, status):
        """Set the status of a comparison with id comp_id.

        Args:
            comp_id (string): Comparison Id.
            status (int): Comparison status.

        Returns:
            dict.
                {
                  "compareId": "string"
                }

        """
        payload = {
            'compareId': comp_id,
            'compareStatus': status
        }
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=logsight.config.HOST_API,
                          path=PATH_POST_STATUS,
                          json=payload,
                          headers=headers)
