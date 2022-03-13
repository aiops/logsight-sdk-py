import click
from prettytable import PrettyTable

from logsight.application import LogsightApplication
from logsight.exceptions import APIException


@click.group('applications')
@click.pass_context
def apps(ctx):
    """Manages applications"""
    pass


@apps.command()
@click.pass_context
def ls(ctx):
    """
    lists applications registered

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr applications ls
    """
    app_mng = LogsightApplication(ctx.obj['USER'].user_id, ctx.obj['USER'].token)
    try:

        table = PrettyTable(['application Id', 'Name'])
        for a in app_mng.lst()['applications']:
            table.add_row([a['applicationId'], a['name']])
        click.echo(table)

    except APIException as e:
        click.echo(f'Unable to retrieve application list ({e})')
        exit(1)

    exit(0)
