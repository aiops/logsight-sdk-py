import logsight.config
from logsight.endpoints import (PATH_POST_INCIDENTS,
                                PATH_GET_INCIDENT_ID,
                                PATH_DELETE_INCIDENT,
                                PATH_POST_INCIDENT_STATUS)
from logsight.api_client import APIClient


class LogsightIncidents(APIClient):

    def __init__(self, token):
        """Class to compare logs.

        Args:
            token (str): Access token.

        """
        super().__init__()
        self.token = token

    def __str__(self):
        return f'token = {self.token}'

    def get_incidents(self, start_time, stop_time):
        """Get a list of incidents given a time range.

        Args:
            start_time (string): Start time of the interval.
            stop_time (string): End time of the interval.

        Returns:
            dict.
                {
                  "listIncident": [
                    {
                      "incidentId": "string",
                      "source": {
                        "countAddedState": 0,
                        "countLevelFault": 0,
                        "countMessages": 0,
                        "countSemanticAnomaly": 0,
                        "countStates": 0,
                        "message": {
                          "addedState": 0,
                          "level": "string",
                          "message": "string",
                          "prediction": 0,
                          "riskScore": 0,
                          "riskSeverity": 0,
                          "tagString": "string",
                          "tags": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string"
                          },
                          "template": "string",
                          "timestamp": "string"
                        },
                        "risk": 0,
                        "severity": 0,
                        "status": 0,
                        "tags": {
                          "additionalProp1": "string",
                          "additionalProp2": "string",
                          "additionalProp3": "string"
                        },
                        "timestamp": "string"
                      }
                    }
                  ]
                }

        """
        payload = {
            'startTime': start_time,
            'stopTime': stop_time
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=logsight.config.HOST_API,
                          path=PATH_POST_INCIDENTS,
                          json=payload,
                          headers=headers)

    def update_incident_status(self, incident_id, status):
        """Compares the logs on an application.

            Args:
                incident_id (string): Incident Id.
                status (int): New status.

        Returns:
            dict.
                {
                  "incidentId": "string"
                }

        """
        payload = {
            'incidentId': incident_id,
            'incidentStatus': status
        }
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._post(host=logsight.config.HOST_API,
                          path=PATH_POST_INCIDENT_STATUS,
                          json=payload,
                          headers=headers)

    def get_incident_id(self, incident_id):
        """Get incident with id incident_id.

        Args:
            incident_id (string): Incident Id.

        Returns:
            dict.
                {
                  "incidentData": {
                    "incidentId": "string",
                    "source": {
                      "countAddedState": 0,
                      "countLevelFault": 0,
                      "countMessages": 0,
                      "countSemanticAnomaly": 0,
                      "countStates": 0,
                      "data": [
                        {
                          "addedState": 0,
                          "level": "string",
                          "message": "string",
                          "prediction": 0,
                          "riskScore": 0,
                          "riskSeverity": 0,
                          "tagString": "string",
                          "tags": {
                            "additionalProp1": "string",
                            "additionalProp2": "string",
                            "additionalProp3": "string"
                          },
                          "template": "string",
                          "timestamp": "string"
                        }
                      ],
                      "message": {
                        "addedState": 0,
                        "level": "string",
                        "message": "string",
                        "prediction": 0,
                        "riskScore": 0,
                        "riskSeverity": 0,
                        "tagString": "string",
                        "tags": {
                          "additionalProp1": "string",
                          "additionalProp2": "string",
                          "additionalProp3": "string"
                        },
                        "template": "string",
                        "timestamp": "string"
                      },
                      "risk": 0,
                      "severity": 0,
                      "status": 0,
                      "tags": {
                        "additionalProp1": "string",
                        "additionalProp2": "string",
                        "additionalProp3": "string"
                      },
                      "timestamp": "string"
                    }
                  }
                }

        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._get(host=logsight.config.HOST_API,
                         path=PATH_GET_INCIDENT_ID.format(incidentId=incident_id),
                         headers=headers)

    def rm_incident_id(self, incident_id):
        """Remove incident with id incident_id.

        Args:
            incident_id (string): Incident Id.

        Returns:
            dict.
                {
                  "incidentId": "string"
                }

        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.token}'
        }
        return self._delete(host=logsight.config.HOST_API,
                            path=PATH_DELETE_INCIDENT.format(incidentId=incident_id),
                            headers=headers,
                            ignore_return_data=False)
