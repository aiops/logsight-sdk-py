import unittest

from tests.config import EMAIL, PASSWORD
from logsight.users import LogsightUsers
from logsight.exceptions import Conflict, Unauthorized


class TestUsers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestUsers, cls).setUpClass()

    def test_create_user_exists(self):
        users = LogsightUsers()
        with self.assertRaises(Conflict):
            users.create(email=EMAIL, password=PASSWORD)

    def test_delete_invalid_user_id_token(self):
        users = LogsightUsers()
        with self.assertRaises(Unauthorized):
            users.delete(user_id='INVALID_USER_ID', token='INVALID_TOKEN')


if __name__ == '__main__':
    unittest.main()
