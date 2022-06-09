import time
import unittest

from tests.config import HOST_API, EMAIL, PASSWORD
from tests.utils import generate_singles

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.applications import LogsightApplications
from logsight.compare import LogsightCompare
from logsight.exceptions import Conflict, InternalServerError
from logsight.logs import LogsightLogs

APP_NAME = 'unittest_compare_app'


class TestCompare(unittest.TestCase):
    app_id = None
    tags_v1 = {'system': 'hadoop', 'version': 'v1.0.0'}
    tags_v2 = {'system': 'hadoop', 'version': 'v2.0.0'}
    receipt_id = None

    @classmethod
    def setUpClass(cls):
        super(TestCompare, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplications(cls.auth.user_id, cls.auth.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']
        cls._send_logs()

    @classmethod
    def tearDownClass(cls):
        cls.app_mng.delete(cls.app_id)

    @classmethod
    def _send_logs(cls):
        n_log_messages = 60
        g = LogsightLogs(cls.auth.token)
        g.send_singles(generate_singles(tags=cls.tags_v1, app_id=cls.app_id, delta=0, n=n_log_messages))
        r = g.send_singles(generate_singles(tags=cls.tags_v2, app_id=cls.app_id, delta=-2, n=n_log_messages))[0]
        cls.receipt_id = r['receiptId']

    @classmethod
    def _retry_compare(cls, comp, baseline_tags, candidate_tags, receipt_id):
        attempt, max_attempts = 0, 5
        r = None
        while attempt < max_attempts:
            try:
                r = comp.compare(baseline_tags=baseline_tags,
                                 candidate_tags=candidate_tags,
                                 log_receipt_id=receipt_id)
                break
            except Conflict:
                time.sleep(1)
                attempt += 1
            except InternalServerError:
                time.sleep(1)
                attempt += 1
        return r

    def test_compare(self):
        comp = LogsightCompare(self.auth.token)
        r = self._retry_compare(comp, self.tags_v1, self.tags_v2, self.receipt_id)

        self.assertIsInstance(r, dict)
        self.assertTrue('totalLogCount' in r)
        self.assertTrue('risk' in r)

    def test_ls_comparisons(self):
        comp = LogsightCompare(self.auth.token)
        r = comp.ls_comparisons()

        self.assertIsInstance(r, dict)
        self.assertTrue('listCompare' in r)
        self.assertIsInstance(r['listCompare'], list)

    def test_create_delete_comparison(self):
        comp = LogsightCompare(self.auth.token)
        r1 = self._retry_compare(comp, self.tags_v1, self.tags_v2, self.receipt_id)
        comp.rm_comparison_id(r1['compareId'])
        r2 = comp.ls_comparisons()
        self.assertFalse(any(i for i in r2['listCompare'] if i['_id'] == r1['compareId']))

    def test_compare_status(self):
        comp = LogsightCompare(self.auth.token)
        r1 = self._retry_compare(comp, self.tags_v1, self.tags_v2, self.receipt_id)

        self.assertIsInstance(r1, dict)
        self.assertTrue('compareId' in r1)
        self.assertIsInstance(r1['compareId'], str)

        # changing the status to 1 give an error since currently it is not possible
        # to update status to the same value. To be fixed at the server level
        r2 = comp.set_status(comp_id=r1['compareId'], status=2)

        self.assertIsInstance(r2, dict)
        self.assertTrue('compareId' in r2)
        self.assertIsInstance(r2['compareId'], str)


if __name__ == '__main__':
    unittest.main()
