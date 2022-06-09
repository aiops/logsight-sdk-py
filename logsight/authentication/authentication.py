import logsight.config
from logsight.endpoints import PATH_AUTH_LOGIN
from logsight.api_client import APIClient


class LogsightAuthentication(APIClient):

    def __init__(self, email, password):
        """Class to authenticate users.

        Args:
            email (str): Email associated with the subscription.
            password (str): Password key associated with the subscription.

        """
        super().__init__()
        self.email = email
        self.password = password
        self._user_id = None
        self._token = None

    def __str__(self):
        return f'email = {self.email}, user id = {self._user_id}, ' \
               f'token = {self._token}'

    def _authenticate(self):
        """Authenticate the user.

        Returns:
            token (str): Access token
            user_id (str): Identifier of the user
        """
        payload = {"email": self.email,
                   "password": self.password}
        headers = {"content-type": "application/json"}
        r = self._post(logsight.config.HOST_API,
                       PATH_AUTH_LOGIN,
                       json=payload,
                       headers=headers)

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
