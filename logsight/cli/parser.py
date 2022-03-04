import dateutil.parser
from datetime import datetime


# open 2 files
# autodetect.py package
# if autodetect: detect datetime format, find delimiter between time / Log Level, and Log Level message
# else: get pattern from cli
# create list of log records

def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def autodetect_datetime(date):
    d = dateutil.parser.parse(date)
    return d, type(d)


def lines_to_struct(lines, field_selector):
    return [line_to_struct(line) for line in lines]


def line_to_struct(line):
    pass


def parse_file(file_name):
    lines = read_lines(file_name)
    field_selector = autodetect_datetime(date)
    return lines_to_struct(lines, field_selector)


if __name__ == '__main__':
    for date in ['Tue, 01 Mar 2016 21:17:00 +0800', '2016/03/01']:
        d, t = autodetect_datetime(date)
        print(d, t)
