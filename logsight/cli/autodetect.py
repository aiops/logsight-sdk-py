import dateutil.parser
from datetime import datetime


def autodetect_datetime(date):
    d = dateutil.parser.parse(date)
    return d, type(d)


if __name__ == '__main__':
    for date in ['Tue, 01 Mar 2016 21:17:00 +0800', '2016/03/01']:
        d, t = autodetect_datetime(date)
        print(d, t)
