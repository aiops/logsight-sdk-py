from logsight.config import HOST_API
from logsight.config import PATH_APP_CREATE, PATH_APP_LST, PATH_APP_DELETE
from logsight.api_client import APIClient


class LogsightApplication(APIClient):

    def __init__(self, user_id, token):
        """Class to manage applications (apps).

        Args:
            user_id (str): Identifier of the user.
            token (str): Access token.

        """
        super().__init__()
        self.user_id = user_id
        self.token = token

    def create(self, app_name):
        """Creates a new application.

        Args:
            app_name (str): Application name.

        Returns:
            dict.
                {
                  "applicationId": "string",
                  "applicationName": "string"
                }

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        return self._post(host=HOST_API,
                          path=PATH_APP_CREATE.format(userId=self.user_id),
                          data={'applicationName': app_name},
                          headers={'Authorization': f'Bearer {self.token}'})

    def lst(self):
        """Lists existing applications.

        Returns:
            dict:
                {
                  "applications": [
                    {
                      "applicationId": "string",
                      "name": "string"
                    }
                  ]
                }

        Raises:
            Unauthorized: If the private_key is invalid.

        """
        return self._get(host=HOST_API,
                         path=PATH_APP_LST.format(userId=self.user_id),
                         headers={'Authorization': f'Bearer {self.token}'})

    def delete(self, app_id):
        """Deletes an existing  application.

        Args:
            app_id (str): Application id.

        Returns:
            dict:
                {
                  "applicationId": "string",
                  "applicationName": "string"
                }

        Raises:
            NotFound: if the app_name does not exist.
            Unauthorized: If the private_key is invalid.

        """
        return self._delete(host=HOST_API,
                            path=PATH_APP_DELETE.format(userId=self.user_id, applicationId=app_id),
                            headers={'Authorization': f'Bearer {self.token}'})
