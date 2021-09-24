import sys
import os
import time
import logging

sys.path.insert(0, '/Users/jcardoso/GitHub/logsight-python-sdk/')

from logsight.exceptions import LogsightException
from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now


PRIVATE_KEY = os.getenv('PRIVATE_KEY') or 'xteitdidb0xd32thtt35ccruy'
APP_NAME = 'quick_start_app'
EMAIL = 'jorge.cardoso.pt@gmail.com'

handler = LogsightLogger(PRIVATE_KEY, EMAIL, APP_NAME)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

filename = os.path.join(os.path.dirname(os.path.abspath(__file__)), './OpenStack_2k.log')
log_records = []
try:
    f = open(filename, 'r')

    level_idx, msg_idx = 4, 5
    for i, line in enumerate(f.readlines()):
        tokens = line.split()
        log_records.append((tokens[level_idx], ' '.join(tokens[msg_idx:])))

except OSError:
    sys.exit("Could not open/read file: %s" % filename)

dt_start = now()
print('Starting message sending', dt_start)

for i, m in enumerate(log_records):
    level, message = m[0].upper(), m[1]
    print(i, level, message)

    mapping = {'INFO': logger.info, 'WARNING': logger.warning, 'ERROR': logger.error, 'DEBUG': logger.debug, 'CRITICAL': logger.critical}

    if level in mapping:
        mapping[level](message)
    else:
        sys.exit('Error parsing level for log message number %d: %s %s' % (i, level, message))

dt_end = now()
print('Ended message sending', dt_end)

handler.close()
logger.removeHandler(handler)

print('Sleeping 60 seconds')
time.sleep(15)

incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
    .get_results(dt_start, dt_end, 'incidents')
real_incidents = sum([1 if i.total_score > 0 else 0 for i in incidents])
print('Number incidents found:', real_incidents)

for i in incidents:
    print('Incident', i)

