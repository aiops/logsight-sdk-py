from logsight.config import HOST_API, PATH_USERS, PATH_LOGIN
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
        self._user_id = None
        self._token = None

    def create(self):
        """Creates a new user.

        Returns:
            userId (str): Identifier for the user created
        """
        data = {"email": self.email, "password": self.password, "repeatPassword": self.password}
        return self._post(HOST_API, PATH_USERS, data)['userId']

    def _authenticate(self):
        """Authenticate the user.

        Returns:
            token (str): Access token
            user_id (str): Identifier of the user
        """
        data = {"email": self.email, "password": self.password}
        r = self._post(HOST_API, PATH_LOGIN, data)

        self._user_id = r['user']['userId']
        self._token = r['token']

    @property
    def token(self):
        """Gets a token.

        Returns:
            token (str): Access token
        """
        if self._token:
            return self._token

        self._authenticate()

        return self._token

    @property
    def user_id(self):
        """Gets the user id.

        Returns:
            user_id (str): Identifier of the user
        """
        if self._user_id:
            return self._user_id

        self._authenticate()

        return self._user_id
