import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.exceptions import (Unauthorized,
                                 NotFound,
                                 ServiceUnavailable)


class TestAuthentication(unittest.TestCase):

    user_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestAuthentication, cls).setUpClass()

    def test_set_invalid_host(self):
        set_host('https://invalid_host_logsight.ai/api/v1/')
        with self.assertRaises(ServiceUnavailable):
            LogsightAuthentication(email=EMAIL, password=PASSWORD).token
        set_host(HOST_API)

    def test_token(self):
        set_host(HOST_API)
        auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        self.assertIsInstance(auth.token, str)

    def test_user_id(self):
        set_host(HOST_API)
        user = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        self.assertIsInstance(user.user_id, str)

    def test_invalid_password(self):
        set_host(HOST_API)
        with self.assertRaises(Unauthorized):
            LogsightAuthentication(email=EMAIL, password='invalid_password').token

    def test_invalid_email(self):
        set_host(HOST_API)
        with self.assertRaises(NotFound):
            LogsightAuthentication(email='invalid_email@invalid.com',
                                   password='at_least_8_characters').token


if __name__ == '__main__':
    unittest.main()
