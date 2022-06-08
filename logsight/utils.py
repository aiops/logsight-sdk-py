import datetime
from dateutil.tz import tzlocal


def now():
    return datetime.datetime.now(tz=tzlocal()).isoformat()
