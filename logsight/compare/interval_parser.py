from datetime import datetime, timedelta
from dateutil.tz import tzlocal
from dateutil import parser

from pyparsing import (
    Word,
    nums,
    Group,
    alphas,
    alphanums,
    Forward,
    Suppress,
    Combine,
    Literal,
    restOfLine,
    CaselessKeyword,
    ParserElement,
    replaceWith,
)


class ParserAppInterval:

    OFFSET, NOW, INTERVAL = map(
        CaselessKeyword, "offset now [".split()
    )
    query_language = Forward()

    def __init__(self):
        ParserElement.enablePackrat()
        self._create_tokens()
        self._create_grammar()
        self._set_options()

    @classmethod
    def _convert_to_seconds(cls, s):
        seconds_per_unit = {"s": 1, "m": 60, "h": 3600, "d": 86400, "w": 604800, "y": 31536000}
        return int(s[:-1]) * seconds_per_unit[s[-1]]

    @classmethod
    def _replace_offset(cls, t):
        seconds = cls._convert_to_seconds(t[0])
        return str((datetime.now(tz=tzlocal()) - timedelta(seconds=seconds)).isoformat())

    @classmethod
    def _replace_interval(cls, t):
        if t[0][0] == cls.INTERVAL:
            seconds = cls._convert_to_seconds(t[0][1])
            date = parser.parse(t[1][0])
            return [[str((date - timedelta(seconds=seconds)).isoformat())], t[1]]
        return t

    def _create_tokens(self):
        self.app_name = Word(alphas, alphanums).setName("app_name")
        self.interval = Literal("[") + Combine(Word(nums) + Word(alphas, exact=1))("interval") + Suppress("]")
        self.timestamp = Suppress(Literal("@")) + Word(alphanums + '-' + ':' + '+')
        self.offset = Suppress(self.OFFSET) + Combine(Word(nums) + Word(alphas, exact=1)).setParseAction(self._replace_offset)
        self.NOW.setParseAction(replaceWith(datetime.now(tz=tzlocal()).isoformat()))

    def _create_grammar(self):
        left_expr = Group(
            self.interval | self.timestamp
        ).setName("left_expression")

        right_expr = Group(
            self.offset | self.timestamp | self.NOW
        ).setName("right_expression")

        self.query_language <<= (
            self.app_name
            + (left_expr + right_expr).setParseAction(self._replace_interval)
        )

    def _set_options(self):
        # enable comments
        self.query_language.ignore("#" + restOfLine)

    def parse(self, expression):
        return self.query_language.parseString(expression)


compare = {
    'app1': ['2021-10-01T07:41:15+00:00', '2021-10-01T07:41:15+00:00'],
    'app2': ['2021-10-01T07:41:15+00:00', '2021-10-01T07:41:15+00:00']
}
