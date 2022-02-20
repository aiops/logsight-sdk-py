from logsight.config import HOST_API, PATH_USERS, PATH_TOKEN
from logsight.api_client import APIClient


class LogsightUser(APIClient):

    def __init__(self, email, password):
        """Class to manage users.

        Args:
            email (str): Email associated with the subscription.
            password (str): Password key associated with the subscription.

        """
        super().__init__()
        self.email = email
        self.password = password

    def create(self):
        """Creates a new user.

        Returns:
            dict: ???.

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        data = {"email": self.email, "password": self.password, "repeatPassword": self.password}
        return self._post(HOST_API, PATH_USERS, data)

    def token(self):
        """Gets a token.

        Returns:
            dict: ???.

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        data = {"email": self.email, "password": self.password}
        return self._post(HOST_API, PATH_TOKEN, data)['token']
