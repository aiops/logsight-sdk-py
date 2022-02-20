import sys
import logging
import logging.handlers
import unittest

# Comments for /compare endpoint
# - GET /api/v1/logs/compare/tags, a) tags are not a particularity of the compare function. They should belong to the endpoint logs/tags
#                                  b) sending logs with tags, and getting the tags immediately return []

# from logsight.exceptions import LogsightException, InternalServerError
# from logsight.utils import now, create_apps, delete_apps

from config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

label2id = {"INFO": 1, "DEBUG": 1, "TRACE": 1, "WARNING": 0, "WARN": 0, "ERROR": 0, "EXCEPTION": 0, "CRITICAL": 0}


def send_logs(logger, i):
    logger.info(f"{i}.1. Hello World!")
    logger.debug(f"{i}.2. Hello Debug!")
    logger.info(f"{i}.3. Hello World!")
    logger.info(f"{i}.4. Hello World!")
    logger.info(f"{i}.5. Hello World!")
    logger.error(f"{i}.6. Hello Error!")
    logger.warning(f"{i}.7. Hello Warning!")
    logger.error(f"{i}.8. Hello Error!")
    logger.warning(f"{i}.9. Hello Warning!")
    logger.debug(f"{i}.10. Hello Debug!")
    logger.info(f"{i}.11. Hello World!")
    logger.info(f"{i}.12. Hello World!")
    logger.info(f"{i}.13. Hello World!")
    logger.info(f"{i}.14. Hello World!")
    logger.info(f"{i}.15. Hello World!")


APP_NAME = 'unittest_compare_app'


class TestLogs(unittest.TestCase):

    app_id = None
    tag_v1 = 'v1.0.0'
    tag_v2 = 'v2.0.0'

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.user.user_id, cls.user.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    @classmethod
    def _generate_logs(cls, day, n=10):
        m = "2022-02-{day:02d} 12:{minutes:02d}:48,963 " \
            "INFO [main] org.apache.hadoop.mapreduce: " \
            "Executing with tokens: {i}"
        return [m.format(day=day, minutes=i, i=i) for i in range(max(n, 60))]

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        g = LogsightLogs(cls.user.token)
        g.send(cls.app_id, cls._generate_logs(day=19, n=n_log_messages), tag=cls.tag_v1)
        g.send(cls.app_id, cls._generate_logs(day=20, n=n_log_messages), tag=cls.tag_v2)

    def test_compare(self):
        c = LogsightCompare(self.user.user_id, self.user.token)\
            .compare(app_id=self.app_id,
                     baseline_tag=self.tag_v1,
                     candidate_tag=self.tag_v2,
                     flush_id=None)
        self.assertIsInstance(c, dict)
        self.assertTrue('totalLogCount' in c)

    def test_tags(self):
        tags = LogsightCompare(self.user.user_id, self.user.token).tags(self.app_id)
        self.assertIsInstance(tags, list)
        self.assertEqual(len(tags), 2)


if __name__ == '__main__':
    unittest.main()
