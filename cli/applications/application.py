import click
from prettytable import PrettyTable

from logsight.application import LogsightApplication
from logsight.exceptions import APIException


@click.group('applications')
@click.pass_context
def apps(ctx):
    """Manages applications"""
    pass


@apps.command('list')
@click.pass_context
def lst(ctx):
    """
    lists applications registered

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr applications list
    """
    app_mng = LogsightApplication(ctx.obj['USER'].user_id, ctx.obj['USER'].token)

    r = None
    try:
        r = app_mng.lst()
    except APIException as e:
        click.echo(f'Unable to retrieve application list ({e})')
        exit(1)

    if r:
        table = PrettyTable(['application Id', 'Name'])
        for a in r['applications']:
            table.add_row([a['applicationId'], a['name']])
        click.echo(table)

    exit(0)
