import unittest
from datetime import datetime

from tests.config import EMAIL, PASSWORD
import logsight.config
from logsight.user import LogsightUser
from logsight.exceptions import (Unauthorized,
                                 NotFound,
                                 ServiceUnavailable)


class TestUserManagement(unittest.TestCase):

    user_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestUserManagement, cls).setUpClass()
        e = 'email_unit_test@' + datetime.now().strftime("%m%d%Y_%H%M%S") + '.com'
        p = 'password.unit.test'
        cls.user_mng = LogsightUser(email=e, password=p)

    def test_set_invalid_host(self):
        logsight.config.set_host('https://invalid_host_logsight.ai/api/v1/')
        with self.assertRaises(ServiceUnavailable):
            LogsightUser(email=EMAIL, password=PASSWORD).token

    def test_token(self):
        user = LogsightUser(email=EMAIL, password=PASSWORD)
        self.assertIsInstance(user.token, str)

    def test_user_id(self):
        user = LogsightUser(email=EMAIL, password=PASSWORD)
        self.assertIsInstance(user.user_id, str)

    def test_invalid_password(self):
        with self.assertRaises(Unauthorized):
            LogsightUser(email=EMAIL, password='invalid_password').token

    def test_invalid_email(self):
        with self.assertRaises(NotFound):
            LogsightUser(email='invalid_email@gmail.com', password='at_least_8_characters').token


if __name__ == '__main__':
    unittest.main()
