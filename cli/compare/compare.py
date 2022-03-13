import sys
import json
import time
import click
from tqdm import tqdm

from logsight.compare import LogsightCompare
from logsight.exceptions import Conflict, BadRequest


N_CALL_RETRIES = 10


@click.group()
@click.pass_context
def compare(ctx):
    """Compares log files"""
    pass


@compare.command()
@click.pass_context
@click.option('--app_id', help='id of the application')
@click.option('--tags', required=True, type=click.Tuple([str, str]), help='tags to use during comparison')
@click.option('--flush_id', help='flush id')
def logs(ctx, app_id, tags, flush_id):
    """
    compare indexed logs

python -m cli.ls-cli compare logs --app_id  07402355-e74e-4115-b21d-4cbf453490d1 --tags v1 v2 --flush_id bbe8e1b3-34f8-414b-bafe-0b6d6092ca26
    """
    u = ctx.obj['USER']

    comp = LogsightCompare(u.user_id, u.token)
    for _ in (td := tqdm(range(1, N_CALL_RETRIES + 1),
                         desc='Call retries',
                         colour='white',
                         file=sys.stdout,
                         disable=not ctx.obj['DEBUG'])):
        td.refresh()
        try:
            r = comp.compare(app_id=app_id,
                             baseline_tag=tags[0],
                             candidate_tag=tags[1],
                             flush_id=flush_id,
                             verbose=ctx.obj['DEBUG'])

            s = json.dumps(r, sort_keys=True, indent=4)
            click.echo(s)
            exit(0)

            break
        except Conflict:
            time.sleep(10)
        except BadRequest as e:
            click.echo(e)
            break

    click.echo('Unable to compare log files')
    exit(1)
