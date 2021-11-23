import html

from logsight.config import HOST_API
from logsight.config import PATH_APP_CREATE, PATH_APP_LST, PATH_APP_DELETE
from logsight.api_client import APIClient


class LogsightApplication(APIClient):

    def __init__(self, private_key, email):
        """Class to manage applications (apps).

        Args:
            private_key (str): Private key associated with the subscription.
            email (str): Private key associated with the subscription.

        """
        super().__init__()
        self.private_key = private_key
        self.email = email

    def create(self, app_name):
        """Creates a new application.

        Args:
            app_name (str): Application name.

        Returns:
            dict: ???.

        Raises:
            BadRequest: if the app_name is invalid, it is duplicated, or
                too the maximum number of applications has been reached
            Unauthorized: If the private_key is invalid.

        """
        data = {"key": self.private_key, "name": app_name}
        return self._post(HOST_API, PATH_APP_CREATE, data)

    def lst(self):
        """Lists existing applications.

        Returns:
            dict: xxxx.

        Raises:
            Unauthorized: If the private_key is invalid.

        """
        payload = {}
        query = f"{self.private_key}"
        return self._get(HOST_API, "/".join([PATH_APP_LST, query]), payload)

    def delete(self, app_id):
        """Deletes an existing  application.

        Args:
            app_id (str): Application name.

        Returns:
            dict: xxxx.

        Raises:
            NotFound: if the app_name does not exist.
            Unauthorized: If the private_key is invalid.

        """
        data = {}
        query = f"{app_id}?key={self.private_key}"
        return self._post(HOST_API, "/".join([PATH_APP_DELETE, query]), data)

    @staticmethod
    def _extract_elasticsearch_error(err):
        start_idx = err.response.text.find("<title>")
        end_idx = err.response.text.find("</title>")

        if start_idx != -1 and end_idx != -1:
            end_idx = end_idx + len("</title>")
            err = (
                str(err)
                + " ("
                + html.unescape(err.response.text[start_idx:end_idx])
                + ")"
            )

        return err
