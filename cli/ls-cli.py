import os
import sys
import json
import time
import datetime
import click
from configparser import ConfigParser
from pathlib import Path
from tqdm import tqdm

import random
import string

from logsight.user import LogsightUser
from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare
from logsight.incidents import LogsightIncident
from logsight.exceptions import APIException, Conflict, NotFound

from cli.transformation import transformation
from cli.applications import application
from cli.compare import compare
from cli.incidents import incidents


config = ConfigParser()
config.read(os.path.join(str(Path.home()), '.logsight'))

# Config file: ~/.logsight
# [DEFAULT]
# EMAIL = 'john.miller@gmail.com'
# USER_ID = '11cc4a8a-c1ff-4852-9486-62fd8e618623'
# PASSWORD = '11whUz-hanpe4-zaqtyr'

CONFIG = {i: None for i in ['EMAIL', 'USERID', 'PASSWORD']}
CONFIG.update({i: config['DEFAULT'][i] for i in CONFIG.keys()
               if config.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})

VERSION = 'v2022.03.11'
N_CALL_RETRIES = 10


def app_name_generator():
    return 'ls_cli_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION)
@click.pass_context
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user.')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user.')
@click.option('--debug/--no-debug', default=False)
def cli(ctx, email, password, debug):
    if not email or not password:
        click.echo(f"Authentication incomplete: EMAIL {'found' if email else 'not found'}, "
                   f"PASSWORD {'found' if email else 'not found'}.")
        exit(1)

    ctx.obj['USER'] = LogsightUser(email=email, password=password)
    ctx.obj['DEBUG'] = debug
    click.echo(f"Debug mode is {'on' if debug else 'off'}")


# @cli.command()
# @click.pass_context
# @click.argument('file1', type=click.Path(exists=True))
# @click.argument('file2', type=click.Path(exists=True))
# @click.option('--tag1', default='v1.0.0', help='tag to assign to log file 1')
# @click.option('--tag2', default='v2.0.0', help='tag to assign to log file 2')
# @click.option('--clean', type=bool, help='Remove the temporary application created')
# def compare(ctx, file1, file2, tag1, tag2, clean):
#     """
#     compare log files by analyzing their states
#
#     FILE1, FILE2 are the name of the log files to compare
#
# python -m cli.ls-cli \
# --email jorge.cardoso.pt@gmail.com \
# --password sawhUz-hanpe4-zaqtyr \
# compare \
# ./tests/integration/fixtures/hadoop_name_node_v1 \
# ./tests/integration/fixtures/hadoop_name_node_v2 \
#  | jq -r '.risk'
#     """
#     u = LogsightUser(email=ctx.obj['EMAIL'], password=ctx.obj['PASSWORD'])
#     app_mng = LogsightApplication(u.user_id, u.token)
#     app_name = app_name_generator()
#
#     app_id = None
#     try:
#         app_id = app_mng.create(app_name)['applicationId']
#     except APIException as e:
#         click.echo(f'Unable to create temporary application ({app_name})')
#         exit(1)
#
#     if ctx.obj['DEBUG']:
#         click.echo(f'app_name: {app_name} (app_id {app_id})')
#
#     logs = LogsightLogs(u.token)
#
#     logs.upload(app_id, file1, tag=tag1)
#     r1 = logs.upload(app_id, file2, tag=tag2)
#
#     flush_id = logs.flush(r1['receiptId'])['flushId']
#
#     comp = LogsightCompare(u.user_id, u.token)
#     r = None
#     for _ in (td := tqdm(range(1, N_CALL_RETRIES + 1),
#                          desc='Call retries',
#                          colour='white',
#                          file=sys.stdout,
#                          disable=not ctx.obj['DEBUG'])):
#         td.refresh()
#         try:
#             r = comp.compare(app_id=app_id,
#                              baseline_tag=tag1,
#                              candidate_tag=tag2,
#                              flush_id=flush_id,
#                              verbose=ctx.obj['DEBUG'])
#             break
#         except Conflict:
#             time.sleep(10)
#         except NotFound:
#             pass
#
#     if clean:
#         app_mng.delete(app_id)
#
#     if r:
#         s = json.dumps(r, sort_keys=True, indent=4)
#         click.echo(s)
#         exit(0)
#     else:
#         click.echo('Unable to compare log files')
#         exit(1)

#
# @cli.command()
# @click.pass_context
# @click.argument('file', type=click.Path(exists=True))
# @click.option('--clean', type=bool, help='Remove the temporary application created')
# def incidents(ctx, file, clean):
#     """
#     show the incidents that occurred in a log file
#
#     FILE is the name of the log file
#
# python -m cli.ls-cli  \
# --email jorge.cardoso.pt@gmail.com \
# --password sawhUz-hanpe4-zaqtyr \
# incidents \
# ./tests/integration/fixtures/hadoop_name_node_v1
#     """
#     tag1 = 'v1.1.1'
#
#     u = LogsightUser(email=ctx.obj['EMAIL'], password=ctx.obj['PASSWORD'])
#     app_mng = LogsightApplication(u.user_id, u.token)
#     app_name = app_name_generator()
#
#     app_id = None
#     try:
#         app_id = app_mng.create(app_name)['applicationId']
#     except APIException as e:
#         click.echo(f'Unable to create temporary application ({app_name})')
#         exit(1)
#
#     if ctx.obj['DEBUG']:
#         click.echo(f'app_name: {app_name} (app_id {app_id})')
#
#     logs = LogsightLogs(u.token)
#
#     r1 = logs.upload(app_id, file, tag=tag1)
#     flush_id = logs.flush(r1['receiptId'])['flushId']
#
#     i = LogsightIncident(u.user_id, u.token)
#     now = datetime.datetime.utcnow()
#     stop_time = now.isoformat()
#     start_time = (now - datetime.timedelta(days=1)).isoformat()
#
#     r = None
#     for _ in (td := tqdm(range(1, N_CALL_RETRIES + 1),
#                          desc='Call retries',
#                          colour='white',
#                          file=sys.stdout,
#                          disable=not ctx.obj['DEBUG'])):
#         td.refresh()
#         try:
#             r = i.incidents(app_id=app_id,
#                             start_time=start_time,
#                             stop_time=stop_time,
#                             flush_id=flush_id,
#                             verbose=ctx.obj['DEBUG'])
#             break
#         except Conflict:
#             time.sleep(10)
#
#     if clean:
#         app_mng.delete(app_id)
#
#     if r:
#         s = json.dumps(r, sort_keys=True, indent=4)
#         click.echo(s)
#         exit(0)
#     else:
#         click.echo('Unable to retrieve incidents')
#         exit(1)


cli.add_command(compare.compare)
cli.add_command(incidents.incidents)
cli.add_command(transformation.transform)
cli.add_command(application.apps)


if __name__ == "__main__":
    cli(obj={})
