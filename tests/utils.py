import datetime
from dateutil.tz import tzlocal


def create_log_record(level, message, timestamp=None, metadata=None):
    timestamp = timestamp or datetime.datetime.now(tz=tzlocal()).isoformat()
    return {
        'timestamp': timestamp,
        'level': level,
        'message': message,
        'metadata': metadata or '',
    }


def generate_logs(delta=0, n=10):
    """ Generate logs using (a variation of) iso8106 format """
    m = "[main] org.apache.hadoop.mapreduce: " \
        "Failed to connect. Executing with tokens: {i}"
    now = datetime.datetime.now(tz=tzlocal())
    d = now + datetime.timedelta(days=delta)
    logs = [create_log_record(timestamp=d.isoformat(),
                              level='INFO',
                              message=m.format(i=i),
                              metadata='') for i in range(max(n, 60))]
    return logs
