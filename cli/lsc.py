import os
import json
import time
import datetime
import click
from configparser import ConfigParser
from pathlib import Path

import random
import string

from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare
from logsight.incidents import LogsightIncident
from logsight.exceptions import Conflict

from cli.log_parser import parse_line


config = ConfigParser()
config.read(os.path.join(str(Path.home()), '.logsight'))

CONFIG = {i: None for i in ['EMAIL', 'USERID', 'PASSWORD']}
CONFIG.update({i: config['DEFAULT'][i] for i in CONFIG.keys()
               if config.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})


def app_name_generator():
    return 'cli_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


@click.group()
def cli():
    pass

# python -m cli.ls compare ./tests/integration/fixtures/hadoop_name_node_v1 \
# ./tests/integration/fixtures/hadoop_name_node_v2 \
# --email jorge.cardoso.pt@gmail.com \
# --password 'sawhUz-hanpe4-zaqtyr' \
# --sep ' ' --date 0 1 --level 2 2 --message 3


@click.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user')
@click.option('--clean', type=bool, help='Remove the temporary application created')
def compare(file1,
            file2,
            email,
            password,
            clean):
    """
    compare log files by analyzing their states

    FILE1, FILE2 are the name of the log files to compare
    """
    tag1 = 'v1.1.1'
    tag2 = 'v2.2.2'

    u = LogsightUser(email=email, password=password)
    app_mng = LogsightApplication(u.user_id, u.token)
    app_name = app_name_generator()
    app_id = app_mng.create(app_name)['applicationId']
    click.echo(f'app_name: {app_name} (app_id {app_id})')

    logs = LogsightLogs(u.token)

    logs.upload(app_id, file1, tag=tag1)
    r1 = logs.upload(app_id, file2, tag=tag2)

    flush_id = logs.flush(r1['receiptId'])['flushId']

    comp = LogsightCompare(u.user_id, u.token)
    while True:
        try:
            r = comp.compare(app_id=app_id,
                             baseline_tag=tag1,
                             candidate_tag=tag2,
                             flush_id=flush_id)
            break
        except Conflict:
            time.sleep(10)

    if clean:
        app_mng.delete(app_id)

    s = json.dumps(r, sort_keys=True, indent=4)
    click.echo(s)


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', required=True, default=' ', type=str, help='name of the output file')
@click.option('--sep', required=False, default=' ', type=str, help='separator used to break log line into array')
@click.option('--date', required=True, type=click.Tuple([int, int]), help='indices of array with the date/time')
@click.option('--level', required=True, type=click.Tuple([int, int]), help='indices of array with log level')
@click.option('--message', required=True, type=int, help='index of array where message starts')
def transform(file,
              output,
              sep,
              date,
              level,
              message):
    """
    transforms the structure of a log file

    FILE, the name of the log file to transform
    """

    with open(file) as r, open(output, 'w') as w:
        for line in r:
            d = parse_line(
                line,
                sep=sep,
                timestamp=lambda x: x[date[0]:date[1]],
                level=lambda x: x[level[0]:level[1]],
                message=lambda x: x[message:])
            if d:
                w.write(' '.join([d[i] for i in ['timestamp', 'level', 'message']]) + '\n')


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user')
@click.option('--clean', type=bool, help='Remove the temporary application created')
def incidents(file,
              email,
              password,
              clean):
    """
    show the incidents that occurred in a log file

    FILE is the name of the log file
    """
    tag1 = 'v1.1.1'

    u = LogsightUser(email=email, password=password)
    app_mng = LogsightApplication(u.user_id, u.token)
    app_name = app_name_generator()
    app_id = app_mng.create(app_name)['applicationId']
    click.echo(f'app_name: {app_name} (app_id {app_id})')

    logs = LogsightLogs(u.token)

    r1 = logs.upload(app_id, file, tag=tag1)
    flush_id = logs.flush(r1['receiptId'])['flushId']

    i = LogsightIncident(u.user_id, u.token)
    now = datetime.datetime.utcnow()
    stop_time = now.isoformat()
    start_time = (now - datetime.timedelta(days=1)).isoformat()

    while True:
        try:
            r = i.incidents(app_id=app_id,
                            start_time=start_time,
                            stop_time=stop_time,
                            flush_id=flush_id)
            break
        except Conflict:
            time.sleep(10)

    if clean:
        app_mng.delete(app_id)

    s = json.dumps(r, sort_keys=True, indent=4)
    click.echo(s)


cli.add_command(transform)
cli.add_command(compare)
cli.add_command(incidents)


if __name__ == "__main__":
    cli()
