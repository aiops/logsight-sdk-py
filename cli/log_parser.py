import dateutil.parser
import datetime


def create_log_record(level, message, timestamp=None, metadata=None):
    return {
        'timestamp': timestamp or datetime.datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z',
        # 'timestamp': timestamp or datetime.datetime.now(tz=tzlocal()).isoformat(),
        'level': level,
        'message': message,
        'metadata': metadata or '',
    }


def read_lines(file_name):
    with open(file_name) as f:
        lines = f.readlines()
    return lines


def autodetect_datetime(date):
    return dateutil.parser.parse(date).strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'


def lines_to_struct(lines, **kwargs):
    return [line_to_struct(line, **kwargs) for line in lines]


def line_to_struct(line, sep, timestamp, level, message):
    t = line.split(sep=sep)
    return create_log_record(timestamp=autodetect_datetime(sep.join(timestamp(t))),
                             level=sep.join(level(t)),
                             message=sep.join(message(t)),
                             metadata='')


def parse_file(file_name, **kwargs):
    lines = read_lines(file_name)
    return lines_to_struct(lines, **kwargs)


if __name__ == '__main__':
    file = '/home/jcardoso/Code/logsight-sdk-py/tests/integration/fixtures/OpenStack_2k.log'
    # --date 1,3
    r = parse_file(file, sep=' ', timestamp=lambda x: x[1:3], level=lambda x: x[4:5], message=lambda x: x[6:])
    for i in r:
        print(i)
