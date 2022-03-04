from typing import Optional, Union
import os
import json
import time
import click
from configparser import ConfigParser
from pathlib import Path

import random
import string

from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare
from logsight.exceptions import Conflict

from cli.log_parser import parse_file


config = ConfigParser()
config.read(os.path.join(str(Path.home()), '.logsight'))

CONFIG = {i: None for i in ['EMAIL', 'USERID', 'PASSWORD']}
CONFIG.update({i: config['DEFAULT'][i] for i in CONFIG.keys()
               if config.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})


@click.group()
def cli():
    pass


@click.command()
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user')
@click.option('--sep', required=False, default=' ', type=str, help='separator used to break log line into array')
@click.option('--date', required=True, type=click.Tuple([int, int]), help='indices of array with the date/time')
@click.option('--level', required=True, type=click.Tuple([int, int]), help='indices of array with log level')
@click.option('--message', required=True, type=int, help='index of array where message starts')
@click.option('--clean', type=bool, help='Remove the application created')
def diff(file1,
         file2,
         email,
         password,
         sep,
         date,
         level,
         message,
         clean):
    """
    compare log files by analyzing their states

    FILE1, FILE2 are the name of the log files to compare
    """
    # click.echo(f'file1: {click.format_filename(file1)}, file2: {click.format_filename(file2)}')
    # click.echo(f'email: {email}, password: {password}')

    logs1 = parse_file(file1,
                       sep=sep,
                       timestamp=lambda x: x[date[0]:date[1]],
                       level=lambda x: x[level[0]:level[1]],
                       message=lambda x: x[message:])
    logs2 = parse_file(file1,
                       sep=sep,
                       timestamp=lambda x: x[date[0]:date[1]],
                       level=lambda x: x[level[0]:level[1]],
                       message=lambda x: x[message:])

    app_name = 'cli_diff_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))
    tag1 = 'v1.1.1'
    tag2 = 'v2.2.2'

    u = LogsightUser(email=email, password=password)
    app_mng = LogsightApplication(u.user_id, u.token)
    app_id = app_mng.create(app_name)['applicationId']

    logs = LogsightLogs(u.token)

    logs.send(app_id, logs1, tag=tag1)
    r1 = logs.send(app_id, logs2, tag=tag2)
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
def incidents():
    """
    show the incidents that occurred in a log file

    FILE is the name of the log file
    """
    pass


@click.command()
def sentiment():
    """
    identifies the semantic of a log line

    LINE is the log line
    """
    pass


cli.add_command(diff)
cli.add_command(incidents)
cli.add_command(sentiment)


if __name__ == "__main__":
    cli()
