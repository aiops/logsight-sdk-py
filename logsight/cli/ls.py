from typing import Optional, Union
import os
import click


@click.group()
def cli():
    pass


@click.command()
@click.argument("file_a", type=click.Path(exists=True))
@click.argument("file_b", type=click.Path(exists=True))
@click.option("--email", default=os.environ['PATH'][:10], help='help')
@click.option("--password", default=os.environ['PATH'][:10], help='help')
@click.option("--autodetect", default=True, help='help')
def diff(file_a: str,
         file_b: str,
         email: Union[str, None],
         password: Union[str, None],
         autodetect: bool = True):
    """
    compare log files by analyzing their states

    FILE_A, File_B are the name of the log files to compare
    """

    click.echo(click.format_filename(file_a))
    click.echo(f"email {email}, file_a {file_a}, file_b {file_b}, autodetect {autodetect}")
    # get password and email from .logsight/config or ENV variables
    # get token from logsight(email, passwd)
    # create tmp app (cli_create random string)
    # open 2 files
    # if autodetect: detect datetime format, find delimiter between time / Log Level, and Log Level message
    # else: get pattern from cli
    # send logs from file a with tag=A
    # send log from file b with tab=B
    # flush
    # pool until logs are stored
    # delete tmp app


@click.command()
def incidents():
    """
    show the incidents that occurred in a log file

    FILE is the name of the log file
    """
    pass


@click.command()
def sentiment():
    """
    identifies the semantic of a log line

    LINE is the log line
    """
    pass


cli.add_command(diff)
cli.add_command(incidents)
cli.add_command(sentiment)


if __name__ == "__main__":
    cli()
