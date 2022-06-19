import unittest
import datetime
from dateutil.tz import tzlocal

from tests.config import HOST_API, EMAIL, PASSWORD

from logsight.config import set_host
from logsight.authentication import LogsightAuthentication
from logsight.incidents import LogsightIncidents

from logsight.exceptions import (NotFound,
                                 InternalServerError)


class TestIncidents(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        super(TestIncidents, cls).setUpClass()
        set_host(HOST_API)
        cls.auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
        cls.inc_clt = LogsightIncidents(cls.auth.token)

    def test_get_incidents(self):
        now = datetime.datetime.utcnow()
        start_time = (now - datetime.timedelta(days=365 * 101)).isoformat()
        stop_time = (now - datetime.timedelta(days=365 * 100)).isoformat()

        d = self.inc_clt.get_incidents(start_time, stop_time)
        self.assertEqual(d['incidents'], [])

    def test_update_incident_status_not_found(self):
        incident_id = '-1'
        status = 0
        with self.assertRaises(InternalServerError):
            self.inc_clt.update_incident_status(incident_id, status)

    def test_get_incident_id_not_found(self):
        incident_id = '-1'
        with self.assertRaises(NotFound):
            self.inc_clt.get_incident_id(incident_id)

    def test_rm_incident_id_not_found(self):
        incident_id = '-1'
        with self.assertRaises(InternalServerError):
            self.inc_clt.rm_incident_id(incident_id)
        pass


if __name__ == '__main__':
    unittest.main()
