import sys
import os
from itertools import cycle
import ntpath


LOG_FILES = {
    'hadoop': os.path.join(os.path.dirname(os.path.abspath(__file__)), './fixtures/Hadoop_2k.log'),
    'openstack': os.path.join(os.path.dirname(os.path.abspath(__file__)), './fixtures/OpenStack_2k.log'),
    'mac': os.path.join(os.path.dirname(os.path.abspath(__file__)), './fixtures/Mac_2k.log'),
}


def parse_generic(f, mappings, level_idx, msg_idx, max_log_messages):

    level_msg = []
    for i, line in enumerate(cycle(f.readlines())):
        if i == max_log_messages:
            break

        words = line.split()
        if len(words) < msg_idx:
            sys.exit('Error splitting log message number %d: %s' % (i, line))

        level = mappings[words[level_idx]] if level_idx else 'INFO'
        level_msg.append((level, ' '.join(words[msg_idx:])))

    return level_msg


def parse_hadoop(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARN': 'WARNING',
        'ERROR': 'ERROR',
    }
    level_idx, msg_idx = 2, 3
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


def parse_openstack(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARNING': 'WARNING',
        'ERROR': 'ERROR',
    }
    level_idx, msg_idx = 4, 5
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


def parse_mac(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARNING': 'WARNING',
        'ERROR': 'ERROR',
    }
    level_idx, msg_idx = None, 3
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


PARSERS = {
    "hadoop": parse_hadoop,
    "openstack": parse_openstack,
    "mac": parse_mac,
}


def load_log_file(filename, max_log_messages):
    try:
        name, _ = os.path.splitext(ntpath.basename(filename))
        parse = PARSERS[name.split('_')[0].lower()]
    except KeyError as e:
        raise RuntimeError(f'No parser found: {e}')
    except Exception as e:
        raise RuntimeError(f'Log filename does not follow the convention: {e}')

    try:
        f = open(filename, 'r')
    except OSError:
        sys.exit("Could not open/read file: %s" % filename)

    with f:
        return parse(f, max_log_messages)


if __name__ == '__main__':
    max_log_messages = 300
    a = load_log_file(LOG_FILES['hadoop'], max_log_messages)
    print(a[:10])
    a = load_log_file(LOG_FILES['openstack'], max_log_messages)
    print(a[:10])
    a = load_log_file(LOG_FILES['mac'], max_log_messages)
    print(a[:10])
