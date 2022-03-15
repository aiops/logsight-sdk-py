import click

from cli.transformation.log_parser import parse_line


@click.command()
@click.argument('file', type=click.Path(exists=True))
@click.option('--output', required=True, default=' ', type=str, help='name of the output file')
@click.option('--date', required=True, type=click.Tuple([int, int]), help='indices of array with the date/time')
@click.option('--level', required=True, type=click.Tuple([int, int]), help='indices of array with log level')
@click.option('--message', required=True, type=int, help='index of array where message starts')
def transform(file, output, date, level, message):
    """
    transforms the structure of a log file

    FILE, the name of the log file to transform

python -m cli.ls-cli transform \
./tests/integration/fixtures/Mac_2k.log \
--output ./tests/integration/fixtures/Mac_2k \
--date 0 3 \
--level 3 3 \
--message 3
    """

    with open(file, 'r') as r, open(output, 'w') as w:
        for line in r:
            d = parse_line(
                line,
                timestamp=lambda x: x[date[0]:date[1]],
                level=lambda x: x[level[0]:level[1]],
                message=lambda x: x[message:])
            if d:
                w.write(' '.join([d[i] for i in ['timestamp', 'level', 'message']]) + r.newlines)
