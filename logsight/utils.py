import datetime
from dateutil.tz import tzlocal


def n_seconds_ago(seconds=60):
    return (datetime.datetime.now(tz=tzlocal()) - datetime.timedelta(seconds=seconds)).isoformat()


def now():
    return datetime.datetime.now(tz=tzlocal()).isoformat()

