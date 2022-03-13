import sys
import json
import time
import datetime
import click
from tqdm import tqdm

import random
import string

from logsight.application import LogsightApplication
from logsight.logs import LogsightLogs
from logsight.incidents import LogsightIncident
from logsight.exceptions import APIException, Conflict

N_CALL_RETRIES = 10


def app_name_generator():
    return 'ls_cli_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))


@click.group()
@click.pass_context
def incidents(ctx):
    """Compares log files"""
    pass


@incidents.command()
@click.pass_context
@click.argument('file', type=click.Path(exists=True))
@click.option('--clean', type=bool, help='Remove the temporary application created')
def get(ctx, file, clean):
    """
    show the incidents that occurred in a log file

    FILE is the name of the log file

python -m cli.ls-cli  \
--email jorge.cardoso.pt@gmail.com \
--password sawhUz-hanpe4-zaqtyr \
incidents get \
./tests/integration/fixtures/hadoop_name_node_v1
    """
    tag1 = 'v1.1.1'

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

    r1 = logs.upload(app_id, file, tag=tag1)
    flush_id = logs.flush(r1['receiptId'])['flushId']

    i = LogsightIncident(u.user_id, u.token)
    now = datetime.datetime.utcnow()
    stop_time = now.isoformat()
    start_time = (now - datetime.timedelta(days=1)).isoformat()

    r = None
    for _ in (td := tqdm(range(1, N_CALL_RETRIES + 1),
                         desc='Call retries',
                         colour='white',
                         file=sys.stdout,
                         disable=not ctx.obj['DEBUG'])):
        td.refresh()
        try:
            r = i.incidents(app_id=app_id,
                            start_time=start_time,
                            stop_time=stop_time,
                            flush_id=flush_id,
                            verbose=ctx.obj['DEBUG'])
            break
        except Conflict:
            time.sleep(10)

    if clean:
        app_mng.delete(app_id)

    if r:
        s = json.dumps(r, sort_keys=True, indent=4)
        click.echo(s)
        exit(0)
    else:
        click.echo('Unable to retrieve incidents')
        exit(1)
