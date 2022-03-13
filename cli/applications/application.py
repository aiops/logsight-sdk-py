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
    python -m cli.ls-cli applications ls
    """
    u = ctx.obj['USER']

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        table = PrettyTable(['application Id', 'Name'])
        for a in app_mng.lst()['applications']:
            table.add_row([a['applicationId'], a['name']])
        click.echo(table)

    except APIException as e:
        click.echo(f'Unable to retrieve application list ({e})')
        exit(1)

    exit(0)


@apps.command()
@click.pass_context
@click.option('--name', help='name of the application.')
def create(ctx, name):
    """
    creates an application

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr applications create --name xxxx
    """
    u = ctx.obj['USER']

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        r = app_mng.create(name)
        click.echo(f"application_id: {r['applicationId']}")

    except APIException as e:
        click.echo(f'Unable to create application name: {name}')
        exit(1)

    exit(0)
