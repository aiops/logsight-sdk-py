import os
import click
from configparser import ConfigParser
from pathlib import Path

from logsight.user import LogsightUser

from cli.applications import application
from cli.logs import logs
from cli.compare import compare
from cli.incidents import incidents
from cli.transformation import transformation


CONFIG_FILE = os.path.join(str(Path.home()), '.logsight')
config = ConfigParser()
config.read(CONFIG_FILE)

# Config file: ~/.logsight
# [DEFAULT]
# EMAIL = john.miller@gmail.com
# USER_ID = 11cc4a8a-c1ff-4852-9486-62fd8e618623
# PASSWORD = 11whUz-hanpe4-zaqtyr

CONFIG = {i: None for i in ['EMAIL', 'USERID', 'PASSWORD']}
CONFIG.update({i: config['DEFAULT'][i] for i in CONFIG.keys()
               if config.has_option('DEFAULT', i)})
CONFIG.update({i: os.environ[f'LOGSIGHT_{i}'] for i in CONFIG.keys()
               if f'LOGSIGHT_{i}' in os.environ})

VERSION = 'v2022.03.11'


@click.group(help="CLI tool to manage logsight.ai artifacts")
@click.version_option(VERSION)
@click.pass_context
@click.option('--debug/--no-debug', default=False)
@click.option('--email', default=CONFIG['EMAIL'], help='email of logsight user.')
@click.option('--password', default=CONFIG['PASSWORD'], help='password of logsight user.')
def cli(ctx, email, password, debug):
    if not email or not password:
        click.echo(f"Authentication incomplete: EMAIL {'found' if email else 'not found'}, "
                   f"PASSWORD {'found' if email else 'not found'}.")
        exit(1)

    ctx.obj['USER'] = LogsightUser(email=email, password=password)
    ctx.obj['DEBUG'] = debug

    if debug:
        click.echo(f"Config file found? {'yes' if Path(CONFIG_FILE).is_file() else 'no'}")
        click.echo(f"EMAIL: {email}, PASSWD: {password}")


cli.add_command(application.apps)
cli.add_command(logs.logs)
cli.add_command(compare.compare)
cli.add_command(incidents.incidents)
cli.add_command(transformation.transform)


if __name__ == "__main__":
    cli(obj={})
