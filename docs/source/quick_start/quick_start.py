import os
import sys
import time
import logging

from logsight.logger import LogsightLogger
from logsight.result import LogsightResult
from logsight.utils import now


PRIVATE_KEY = os.getenv('LOGSIGHT_PRIVATE_KEY') or 'mgewxky59zm1euavowtjon9igc'
EMAIL = os.getenv('LOGSIGHT_EMAIL') or 'jorge.cardoso.pt@gmail.com'

APP_NAME = 'quick_start_app'

handler = LogsightLogger(PRIVATE_KEY, EMAIL, APP_NAME)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)

log_records = []
try:
    f = open('Hadoop_2k.log', 'r')

    for i, line in enumerate(f.readlines()):
        tokens = line.split()
        level_idx, msg_idx = 2, 3
        log_records.append((tokens[level_idx], ' '.join(tokens[msg_idx:])))

except OSError:
    sys.exit('Could not open/read file')

dt_start = now()
print('Starting log records sending', dt_start)

mapping = {'INFO': logger.info, 'WARNING': logger.warning, 'WARN': logger.warning,
           'ERROR': logger.error, 'DEBUG': logger.debug, 'CRITICAL': logger.critical,
           'FATAL': logger.critical}

for i, m in enumerate(log_records):
    level, message = m[0].upper(), m[1]
    print(i, level, message)

    if level in mapping:
        mapping[level](message)
    else:
        sys.exit('Unknown log level. Log record number %d: %s %s' % (i, level, message))

handler.flush()

dt_end = now()
print('Ended log records sending', dt_end)

sleep_time = 60
print(f'Sleeping {sleep_time} seconds')
time.sleep(sleep_time)

incidents = LogsightResult(PRIVATE_KEY, EMAIL, APP_NAME)\
    .get_results(dt_start, dt_end, 'incidents')

for j, i in enumerate(incidents):
    print('Incident:', j + 1, 'Score:', i.total_score, '(', i.timestamp_start, i.timestamp_end, ')')
