from dateutil.tz import tzlocal
import unittest
from ddt import ddt, data, unpack
from testfixtures import Replace, test_datetime

from logsight.compare.interval_parser import ParserAppInterval

TEST_CASES = [
    ("App1 [5m] now",
     ['App1', ['1978-06-29T14:55:00+01:00'], ['1978-06-29T15:00:00+01:00']]),
    ("App1 [5m] offset 4w",
     ['App1', ['1978-06-01T14:55:00+01:00'], ['1978-06-01T15:00:00+01:00']]),
    ("App1 [5m] @ 2021-10-01T07:41:15+01:00",
     ['App1', ['2021-10-01T07:36:15+01:00'], ['2021-10-01T07:41:15+01:00']]),
    ("App1 @ 2021-10-01T07:41:15+01:00 offset 4w",
     ['App1', ['2021-10-01T07:41:15+01:00'], ['1978-06-01T15:00:00+01:00']]),
    ("App1 @ 1978-06-29T14:55:00+01:00 @ 1978-06-29T15:00:00+01:00",
     ['App1', ['1978-06-29T14:55:00+01:00'], ['1978-06-29T15:00:00+01:00']])
]


@ddt
class TestQueries(unittest.TestCase):

    @data(*TEST_CASES)
    def test_queries(self, test_case):

        with Replace('logsight.compare.interval_parser.datetime',
                     test_datetime(1978, 6, 29, 15, 0, 0, delta=0, tzinfo=tzlocal())):

            ql = ParserAppInterval()
            query, expected = test_case[0], test_case[1]
            _, start, end = ql.parse(query)
            self.assertEqual(start[0], expected[1][0])
            self.assertEqual(end[0], expected[2][0])


if __name__ == '__main__':
    unittest.main()
