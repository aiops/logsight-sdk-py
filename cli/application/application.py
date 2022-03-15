import click
from prettytable import PrettyTable

from logsight.application import LogsightApplication
from logsight.exceptions import APIException


@click.group('application')
@click.pass_context
def apps(ctx):
    """Manages applications"""
    pass


@apps.command()
@click.pass_context
def ls(ctx):
    """
    lists applications registered

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr application ls
    python -m cli.ls-cli application ls
    """
    u = ctx.obj['USER']

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        table = PrettyTable(['APPLICATION ID', 'NAME'])
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

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr application create --name xxxx
    """
    u = ctx.obj['USER']

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        r = app_mng.create(name)
        click.echo(f"app_id: {r['applicationId']}")

    except APIException as e:
        click.echo(f'Unable to create application name: {name} ({e})')
        exit(1)

    exit(0)


@apps.command()
@click.pass_context
@click.option('--app_id', help='name of the application.')
def delete(ctx, app_id):
    """
    deletes an application

    python -m cli.ls-cli --email jorge.cardoso.pt@gmail.com --password sawhUz-hanpe4-zaqtyr application delete --app_id xxxx
    """
    u = ctx.obj['USER']
    a = app_id or ctx.obj['APP_ID']

    try:

        app_mng = LogsightApplication(u.user_id, u.token)
        app_mng.delete(a)

    except APIException as e:
        click.echo(f'Unable to delete application name ({e})')
        exit(1)

    exit(0)
