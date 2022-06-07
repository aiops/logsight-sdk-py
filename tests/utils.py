import datetime
from dateutil.tz import tzlocal


# def create_log_record(level, message, timestamp=None, metadata=None):
#     timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
#     return {
#         'timestamp': timestamp,
#         'level': level,
#         'message': message,
#         'metadata': metadata or '',
#     }
#
#
# def generate_logs(delta=0, n=60):
#     """ Generate logs using (a variation of) iso8106 format """
#     m = "[main] org.apache.hadoop.mapreduce: " \
#         "Failed to connect. Executing with tokens: {i}"
#     d = datetime.datetime.now(tz=tzlocal()) + datetime.timedelta(days=delta)
#     logs = [create_log_record(timestamp=d.isoformat(),
#                               level='INFO',
#                               message=m.format(i=i),
#                               metadata='') for i in range(max(n, 60))]
#     return logs


def create_single(app_id, level, message, tags, timestamp=None, metadata=None):
    timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
    r = {
        'applicationId': app_id,
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'tags': tags
    }
    if metadata:
        r.update({'metadata': metadata})
    return r


def generate_singles(app_id, tags, delta=0, n=60):
    """ Generate logs using (a variation of) iso8106 format """
    m = "[main] org.apache.hadoop.mapreduce: " \
        "Failed to connect. Executing with tokens: {i}"
    d = datetime.datetime.now(tz=tzlocal()) + datetime.timedelta(days=delta)
    logs = [create_single(app_id=app_id,
                          level='INFO',
                          message=m.format(i=i),
                          tags=tags,
                          timestamp=d.isoformat(),
                          metadata='') for i in range(max(n, 60))]
    return logs
