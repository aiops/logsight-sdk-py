import os
import sys
import json
import time
import click
from tqdm import tqdm

import random
import string

from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.compare import LogsightCompare
from logsight.exceptions import APIException, Conflict, NotFound


N_CALL_RETRIES = 10


def app_name_generator():
    return 'ls_cli_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


@click.group()
@click.pass_context
def compare(ctx):
    """Compares log files"""
    pass


@compare.command()
@click.pass_context
@click.argument('file1', type=click.Path(exists=True))
@click.argument('file2', type=click.Path(exists=True))
@click.option('--tag1', default='v1.0.0', help='tag to assign to log file 1')
@click.option('--tag2', default='v2.0.0', help='tag to assign to log file 2')
@click.option('--clean', type=bool, help='Remove the temporary application created')
def files(ctx, file1, file2, tag1, tag2, clean):
    """
    compare log files by analyzing their states

    FILE1, FILE2 are the name of the log files to compare

python -m cli.ls-cli \
--email jorge.cardoso.pt@gmail.com \
--password sawhUz-hanpe4-zaqtyr \
compare files \
./tests/integration/fixtures/hadoop_name_node_v1 \
./tests/integration/fixtures/hadoop_name_node_v2 \
 | jq -r '.risk'
    """
    u = ctx.obj['USER']
    app_mng = LogsightApplication(u.user_id, u.token)
    app_name = app_name_generator()

    app_id = None
    try:
        app_id = app_mng.create(app_name)['applicationId']
    except APIException as e:
        click.echo(f'Unable to create temporary application ({app_name})')
        exit(1)

    if ctx.obj['DEBUG']:
        click.echo(f'app_name: {app_name} (app_id {app_id})')

    logs = LogsightLogs(u.token)

    logs.upload(app_id, file1, tag=tag1)
    r1 = logs.upload(app_id, file2, tag=tag2)

    flush_id = logs.flush(r1['receiptId'])['flushId']

    comp = LogsightCompare(u.user_id, u.token)
    r = None
    for _ in (td := tqdm(range(1, N_CALL_RETRIES + 1),
                         desc='Call retries',
                         colour='white',
                         file=sys.stdout,
                         disable=not ctx.obj['DEBUG'])):
        td.refresh()
        try:
            r = comp.compare(app_id=app_id,
                             baseline_tag=tag1,
                             candidate_tag=tag2,
                             flush_id=flush_id,
                             verbose=ctx.obj['DEBUG'])
            break
        except Conflict:
            time.sleep(10)
        except NotFound:
            pass

    if clean:
        app_mng.delete(app_id)

    if r:
        s = json.dumps(r, sort_keys=True, indent=4)
        click.echo(s)
        exit(0)
    else:
        click.echo('Unable to compare log files')
        exit(1)


@compare.command()
@click.pass_context
def tags():
    click.echo("Return tags")
