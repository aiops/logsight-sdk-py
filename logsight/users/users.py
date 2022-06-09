import logsight.config
from logsight.endpoints import PATH_USERS, PATH_USERS_DELETE, PATH_AUTH_LOGIN
from logsight.api_client import APIClient


class LogsightUsers(APIClient):

    def __init__(self):
        """Class to manage users."""
        super().__init__()

    def create(self, email, password):
        """Creates a new user.

        Args:
            email (str): Email associated with the subscription.
            password (str): Password key associated with the subscription.
        Returns:
            userId (str): Identifier for the user created
        """
        payload = {"email": email,
                   "password": password,
                   "repeatPassword": password}
        headers = {"content-type": "application/json"}
        return self._post(logsight.config.HOST_API,
                          PATH_USERS,
                          json=payload,
                          headers=headers)['userId']

    def delete(self, user_id, token):
        """Deletes a new user.

        Args:
            userId (str): Identifier for the user
        """
        headers = {
            'content-type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        return self._delete(logsight.config.HOST_API,
                            path=PATH_USERS_DELETE.format(userId=user_id),
                            headers=headers)
