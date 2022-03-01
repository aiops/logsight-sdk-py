import unittest
from datetime import datetime

# Comments for /users endpoint
# - POST /api/v1/users. remove key repeatPassword.

# - POST /api/v1/users/activate. "activationToken": "3fa85f64-5717-4562-b3fc-2c963f66afa6", the type should be string, not a uuid (this issue happens often)
# - POST /api/v1/users/resend_activation -> GET /api/v1/users/activation

# - POST /api/v1/users/change_password   -> PUT /api/v1/users/password (remove repeatNewPassword)

# - POST /api/v1/users/forgot_password   -> GET /api/v1/users/password/reset
# - POST /api/v1/users/reset_password   ->  POST /api/v1/users/password/reset (remove repeatNewPassword; why is userId returned?)

from tests.config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.exceptions import (BadRequest,
                                 Unauthorized,
                                 Conflict)


class TestUserManagement(unittest.TestCase):

    user_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestUserManagement, cls).setUpClass()
        e = 'email_unit_test@' + datetime.now().strftime("%m%d%Y_%H%M%S") + '.com'
        p = 'password.unit.test'
        cls.user_mng = LogsightUser(email=e, password=p)

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
        with self.assertRaises(BadRequest):
            LogsightUser(email='invalid_email@gmail.com', password='at_least_8_characters').token

    def test_create_existing_user(self):
        user_id = self.user_mng.create()
        self.assertIsInstance(user_id, str)
        with self.assertRaises(Conflict):
            self.user_mng.create()

    def test_create_delete(self):
        """TODO(Jorge): Needs to be implemented"""
        pass


if __name__ == '__main__':
    unittest.main()
