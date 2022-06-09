import os
import time
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
handler = LogsightLogger(auth.token, 'my_app')
handler.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)


print('Redis running (v1.1.2)')
tags_1 = {'service': 'redis', 'version': 'v1.1.52'}
handler.set_tags(tags=tags_1)
for i in range(10):
    logger.info(f'Connecting to database (instance ID: {i % 4})')
    logger.info(f'Reading {i * 100} KBytes')
    logger.info(f'Closing connection (instance ID: {i % 4})')
handler.flush()

print('Redis running (v2.1.2)')
tags_2 = {'service': 'redis', 'version': 'v2.1.53'}
handler.set_tags(tags=tags_2)
for i in range(15):
    logger.info(f'Connecting to database (instance ID: {i % 4})')
    logger.info(f'Unable to read {i * 100} KBytes')
    logger.error(f'Underlying storage is corrupted')
    logger.info(f'Closing connection (instance ID: {i % 4})')
handler.flush()

print('Calculate new deployment risk')
comp = LogsightCompare(auth.token)
result = {}
retry = 5
while retry:
    try:
        result = comp.compare(baseline_tags=tags_1, candidate_tags=tags_2)
        break
    except InternalServerError as e:
        print(f'Trying in 5s (#{retry})')
        time.sleep(5)
        retry -= 1

print(f'Deployment risk: {result["risk"]}')
print(f'Report webpage: {result["link"]}')
