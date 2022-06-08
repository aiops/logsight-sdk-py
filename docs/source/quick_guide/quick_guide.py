import os
import time
import json
import logging

from logsight.config import set_host
from logsight.exceptions import InternalServerError
from logsight.authentication import LogsightAuthentication
from logsight.logger.logger import LogsightLogger
from logsight.compare import LogsightCompare

EMAIL = os.getenv('LOGSIGHT_EMAIL') or 'jorge.cardoso.pt@gmail.com'
PASSWORD = os.getenv('LOGSIGHT_PASSWORD') or 'jambus-kujdog-jexGe4'
set_host("https://demo.logsight.ai/api/v1/")

auth = LogsightAuthentication(email=EMAIL, password=PASSWORD)
handler = LogsightLogger(auth.token)
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


print('Version v1.1.2 runs and generates logs')
tags_1 = {'version': 'v1.1.9'}
handler.set_tags(tags=tags_1)
logger.info('Progress of TaskAttempt attempt_1445144423722_0020_m_000001_0 is')
logger.info('abc')
logger.info('abc')

print('Version v2.1.2 runs and generates logs')
tags_2 = {'version': 'v2.1.9'}
handler.set_tags(tags=tags_2)
logger.info('abc2')
logger.info('abc2')
logger.info('abc2')

print('Flush any log record in the logging pipeline')
handler.flush()

print('Verify application v2.1.2 with respect to v1.1.2 ...')
comp = LogsightCompare(auth.token)
retry = 5
while retry:
    try:
        r = comp.compare(baseline_tags=tags_1, candidate_tags=tags_2)
        break
    except InternalServerError as e:
        print(e)
        print(f'Sleeping 5s (#{retry})')
        time.sleep(5)
        retry -= 1

print('Verification results')
print(json.dumps(r, sort_keys=True, indent=4))
