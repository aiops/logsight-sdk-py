from dateutil import parser
from dateutil.tz import tzlocal
import datetime


def create_log_record(level, message, timestamp=None, metadata=None):
    return {
        'timestamp': timestamp or datetime.datetime.now(tz=tzlocal()).isoformat(),
        'level': level,
        'message': message,
        'metadata': metadata or '',
    }


def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def autodetect_datetime(date):
    try:
        return parser.parse(date).replace(tzinfo=tzlocal()).isoformat()
    except parser._parser.ParserError as e:
        return None


def parse_lines(lines, **kwargs):
    return [parse_line(line, **kwargs) for line in lines]


def parse_line(line, timestamp, level, message):
    sep = ' '
    line_lst = line.split()

    d = {'timestamp': autodetect_datetime(sep.join(timestamp(line_lst))),
         'level': sep.join(level(line_lst)) or 'INFO',
         'message': sep.join(message(line_lst)),
         'metadata': ''}

    if not d['timestamp']:
        return None

    return create_log_record(**d)


def parse_file(file_name, **kwargs):
    lines = read_lines(file_name)
    return [i for i in parse_lines(lines, **kwargs) if i is not None]
    # return lines_to_struct(lines, **kwargs)


if __name__ == '__main__':
    # file = '/home/jcardoso/Code/logsight-sdk-py/tests/integration/fixtures/OpenStack_2k.log'
    # r = parse_file(file, sep=' ', timestamp=lambda x: x[1:3], level=lambda x: x[4:5], message=lambda x: x[6:])

    file = '/home/jcardoso/Code/logsight-sdk-py/tests/integration/fixtures/hadoop_name_node_v2'
    r = parse_file(file, sep=' ', timestamp=lambda x: x[0:2], level=lambda x: x[2:3], message=lambda x: x[3:])
    for i in r:
        print(i)
    print(len(r))
