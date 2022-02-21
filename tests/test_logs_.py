import unittest
import datetime
from dateutil.tz import tzlocal
import json

# Comments for /logs endpoint
# - POST /api/v1/logs, a) the key 'logFormats' suggests the log messages may have several formats (plural)
#                      b) Adopt a general keyword for missing/unknown information, e.g., NONE
#                         e.g., "logFormats": "UNKNOWN_FORMAT" -> "NONE"
#

from tests.config import EMAIL, PASSWORD
from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs

from logsight.exceptions import (LogsightException,
                                 Unauthorized,
                                 Forbidden,
                                 BadRequest,
                                 NotFound,
                                 Conflict)

APP_NAME = 'hello_app'


class TestLogs(unittest.TestCase):

    app_id = None

    @classmethod
    def setUpClass(cls):
        super(TestLogs, cls).setUpClass()
        cls.user = LogsightUser(email=EMAIL, password=PASSWORD)
        cls.app_mng = LogsightApplication(cls.user.user_id, cls.user.token)
        cls.app_id = cls.app_mng.create(APP_NAME)['applicationId']

    # @classmethod
    # def tearDownClass(cls):
    #     cls.app_mng.delete(cls.app_id)

    def _generate_logs_iso8106(self, n=10):
        # "Feb  1 18:20:29 kernel: [33160.926181] audit: type=1400 audit(1643736029.672:10417): apparmor=DENIED operation=open profile=snap.whatsapp-for-linux.whatsapp-for-linux name=/proc/zoneinfo pid=58597 comm=PressureMonitor requested_mask=r denied_mask=r fsuid=1000 ouid=0",
        m = "INFO [main] org.apache.hadoop.mapreduce: Executing with tokens: {i}"
        return [json.dumps({'timestamp_iso8601': datetime.datetime.now(tz=tzlocal()).isoformat(),
                            'message': m.format(i=i)}) for i in range(max(n, 60))]

    def _generate_logs_syslog(self, n=10):
        m = 'Feb 21 00:{minutes:02d}:52 jcardoso-HP-EliteDesk-800-G2-TWR kernel: [221038.890620] ' \
            'audit: type=1400 audit(1645398052.765:47782): apparmor="DENIED" operation="open" ' \
            'profile="snap.whatsapp-for-linux.whatsapp-for-linux" name="/proc/zoneinfo" pid=5759 ' \
            'comm="PressureMonitor" requested_mask="r" denied_mask="r" fsuid=1000 ouid={i:02d}'

        m = "Feb 14 17:{minutes:02d}:52 admin kernel: [24652.948683] [UFW BLOCK] IN=wlp2s0 OUT= MAC=01:00:5e:00:00:01:98:9b:cb:c7:bb:33:08:00 SRC=192.168.178.1 DST=224.0.0.1 LEN=32 TOS=0x00 PREC=0xC0 TTL=1 ID=55766 DF PROTO={i:02d}"
        return [m.format(minutes=i, i=i) for i in range(max(n, 60))]

    def test_logs_iso8106(self):
        n_log_messages = 60
        g = LogsightLogs(self.user.token)
        p = self._generate_logs_iso8106(n=n_log_messages)
        r = g.send(self.app_id, p, tag='v1.1.2')
        print(r)
        self.assertEqual(r['logsCount'], n_log_messages)

    def _test_logs_syslog(self):
        n_log_messages = 60
        g = LogsightLogs(self.user.token)
        p = self._generate_logs_syslog(n=n_log_messages)
        r = g.send(self.app_id, p, tag='v1.1.2')
        print(r)
        self.assertEqual(r['logsCount'], n_log_messages)

    # def test_invalid_app_id(self):
    #     n_log_messages = 60
    #     invalid_app_id = 'invalid_app_id'
    #     with self.assertRaises(BadRequest):
    #         LogsightLogs(self.user.token).send(invalid_app_id,
    #                                            self._generate_logs(n=n_log_messages),
    #                                            tag='v1.1.2')


if __name__ == '__main__':
    unittest.main()
