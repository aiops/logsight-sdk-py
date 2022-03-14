import click
from prettytable import PrettyTable

from logsight.logs import LogsightLogs
from logsight.exceptions import APIException
from logsight.compare import LogsightCompare


@click.group()
@click.pass_context
def log(ctx):
    """Operates on log files"""
    pass


@log.command('upload')
@click.pass_context
@click.argument('file', type=click.Path(exists=True))
@click.option('--tag', help='tag to index the log file.')
@click.option('--app_id', help='application id which will receive the log file.')
def upload(ctx, file, tag, app_id):
    """
    Upload a log file to an application

    FILE is the name of the log file

    python -m cli.ls-cli log upload <file> --tag v1 --app_id <applicationId>
    """
    u = ctx.obj['USER']
    a = app_id or ctx.obj['APP_ID']

    flush_id = None
    try:
        logs = LogsightLogs(u.token)
        r = logs.upload(a, file, tag=tag)
        flush_id = logs.flush(r['receiptId'])['flushId']
    except APIException as e:
        click.echo(f'Unable to upload log file to application ({e})')
        exit(1)

    click.echo(f'flush_id: {flush_id}')
    exit(0)


@log.group()
@click.pass_context
def tag(ctx):
    pass


@tag.command()
@click.pass_context
@click.option('--app_id', help='application id which will receive the log file.')
def ls(ctx, app_id):
    """
    List the tags of logs

    python -m cli.ls-cli log tag ls --app_id <applicationId>
    """
    u = ctx.obj['USER']
    a = app_id or ctx.obj['APP_ID']

    try:

        cmp_mng = LogsightCompare(u.user_id, u.token)
        table = PrettyTable(['Tag', 'View'])
        for i in cmp_mng.tags(a):
            table.add_row([i['tag'], i['tagView']])
        click.echo(table)

    except APIException as e:
        click.echo(f'Unable to retrieve tags ({e})')
        exit(1)

    exit(0)
