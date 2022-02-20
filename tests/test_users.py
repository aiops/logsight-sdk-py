import unittest
from datetime import datetime

# Comments for /users endpoint
# - POST /api/v1/users. remove key repeatPassword.
# - missing endpoint: DELETE /api/v1/users

# - POST /api/v1/users/activate. "activationToken": "3fa85f64-5717-4562-b3fc-2c963f66afa6", the type should be string, not a uuid (this issue happens often)
# - POST /api/v1/users/resend_activation -> GET /api/v1/users/activation

# - POST /api/v1/users/change_password   -> PUT /api/v1/users/password (remove repeatNewPassword)

# - POST /api/v1/users/forgot_password   -> GET /api/v1/users/password/reset
# - POST /api/v1/users/reset_password   ->  POST /api/v1/users/password/reset (remove repeatNewPassword; why is userId returned?)

from tests.config import EMAIL, PASSWORD, USER_ID
from logsight.user import LogsightUser
from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)


class TestUserManagement(unittest.TestCase):

    user_mng = None

    @classmethod
    def setUpClass(cls):
        super(TestUserManagement, cls).setUpClass()

        now = datetime.now()

        e = 'email_unit_test@' + now.strftime("%m%d%Y_%H%M%S") + '.com'
        p = 'password.unit.test'
        cls.user_mng = LogsightUser(email=e, password=p)

    def test_create_existing_user(self):

        d = self.user_mng.create()

        self.assertIsInstance(d, dict)
        self.assertIsInstance(d['userId'], str)

        with self.assertRaises(Conflict):
            d = self.user_mng.create()

    def test_token(self):
        user = LogsightUser(email=EMAIL, password=PASSWORD)
        self.assertIsInstance(user.token(), str)


if __name__ == '__main__':
    unittest.main()
