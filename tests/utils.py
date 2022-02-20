import time
from enum import Enum


class SLEEP(Enum):
    AFTER_CREATE_APP = ("Sleeping after creating app:", 90)
    BEFORE_DELETE_APP = ("Sleeping before deleting app:", 90)
    AFTER_SENDING_LOGS = ("Sleeping after sending logs:", 30)
    BEFORE_QUERY_BACKEND = ("Sleeping before querying backend:", 75)


def p_sleep(sleep):
    print(sleep.value[0], sleep.value[1], 'sec')
    time.sleep(sleep.value[1])
