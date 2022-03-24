import sys
import os
from itertools import cycle
import ntpath


ABSPATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
LOG_FILES = {
    'hadoop': os.path.join(ABSPATH, 'Hadoop_2k.log'),
    'openstack': os.path.join(ABSPATH, 'OpenStack_2k.log'),
    'mac': os.path.join(ABSPATH, 'Mac_2k.log'),
    'zookeeper': os.path.join(ABSPATH, 'Zookeeper_2k.log'),
    'openssh': os.path.join(ABSPATH, 'OpenSSH_2k.log'),
    'helloworld': os.path.join(ABSPATH, 'HelloWorld_15.log'),
}


def parse_generic(f, mappings, level_idx, msg_idx, max_log_messages):

    level_msg = []
    for i, line in enumerate(cycle(f.readlines())):
        if i == max_log_messages:
            break

        tokens = line.split()
        if len(tokens) < msg_idx or (level_idx and len(tokens) < level_idx):
            sys.exit('Error splitting log message number %d: %s' % (i, line))

        level = 'INFO'
        if level_idx >= 0:
            if tokens[level_idx] in mappings:
                level = mappings[tokens[level_idx]]
            else:
                sys.exit('Unknown level, line: %d, %s (%s)'
                         % (i, level_idx, f.name))

        level_msg.append((level, ' '.join(tokens[msg_idx:])))

    return level_msg


def parse_zookeeper(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARN': 'WARNING',
        'ERROR': 'ERROR',
    }
    level_idx, msg_idx = 3, 4
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


def parse_openssh(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARN': 'WARNING',
        'ERROR': 'ERROR',
    }
    level_idx, msg_idx = None, 5
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


def parse_hadoop(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARN': 'WARNING',
        'ERROR': 'ERROR',
        'FATAL': 'FATAL',
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


def parse_hello_world(f, max_log_messages):
    mappings = {
        'INFO': 'INFO',
        'WARNING': 'WARNING',
        'ERROR': 'ERROR',
        'DEBUG': 'DEBUG',
    }
    level_idx, msg_idx = 0, 1
    return parse_generic(f, mappings, level_idx, msg_idx, max_log_messages)


PARSERS = {
    "hadoop": parse_hadoop,
    "openstack": parse_openstack,
    "mac": parse_mac,
    "zookeeper": parse_zookeeper,
    "openssh": parse_openssh,
    "helloworld": parse_hello_world,
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
    max_log_messages = 2000
    # a = load_log_file(LOG_FILES['hadoop'], max_log_messages)
    # print(a[:10])
    # a = load_log_file(LOG_FILES['openstack'], max_log_messages)
    # print(a[:10])
    # a = load_log_file(LOG_FILES['mac'], max_log_messages)
    # print(a[:10])
    # a = load_log_file(LOG_FILES['zookeeper'], max_log_messages)
    # print(a[:10])
    # a = load_log_file(LOG_FILES['openssh'], max_log_messages)
    # print(a[:10])
    a = load_log_file(LOG_FILES['helloworld'], max_log_messages)
    print(a[:10])
