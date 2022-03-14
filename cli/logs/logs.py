import click
from prettytable import PrettyTable

from logsight.logs import LogsightLogs
from logsight.exceptions import APIException
from logsight.compare import LogsightCompare


@click.group()
@click.pass_context
def logs(ctx):
    """Operates on log files"""
    pass


@logs.command('upload')
@click.pass_context
@click.argument('file', type=click.Path(exists=True))
@click.option('--tag', help='tag to index the log file.')
@click.option('--app_id', help='application id which will receive the log file.')
def upload(ctx, file, tag, app_id):
    """
    Upload a log file to an application

    FILE is the name of the log file

./tests/integration/fixtures/hadoop_name_node_v1 \

python -m cli.ls-cli logs upload ./tests/integration/fixtures/Hadoop_2k.log --tag v1 \
--app_id 07402355-e74e-4115-b21d-4cbf453490d1
    """
    u = ctx.obj['USER']

    flush_id = None
    try:
        logs = LogsightLogs(u.token)
        r = logs.upload(app_id, file, tag=tag)
        flush_id = logs.flush(r['receiptId'])['flushId']
    except APIException as e:
        click.echo(f'Unable to upload log file to application ({e})')
        exit(1)

    click.echo(f'flush_id: {flush_id}')
    exit(0)


@logs.command()
@click.pass_context
@click.option('--app_id', help='application id which will receive the log file.')
def tags(ctx, application_id):
    """
    Get the tags of logs

    python -m cli.ls-cli logs tags --app_id 07402355-e74e-4115-b21d-4cbf453490d1
    """
    u = ctx.obj['USER']

    try:

        cmp_mng = LogsightCompare(u.user_id, u.token)
        table = PrettyTable(['Tag', 'View'])
        for a in cmp_mng.tags(application_id):
            table.add_row([a['tag'], a['tagView']])
        click.echo(table)

    except APIException as e:
        click.echo(f'Unable to retrieve tags ({e})')
        exit(1)

    exit(0)
