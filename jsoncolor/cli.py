"""Command-Line Interface."""

import sys

import click
import click._termui_impl
from click import argument
from click import option
from click import version_option

from jsoncut.cli import load_json

from jsoncolor.core import format_json
from jsoncolor.core import highlighter


def output(data, ctx, indent):
    try:
        if data:
            if click._termui_impl.isatty(sys.stdin):
                compact = False
                indent = 2 if indent is None else indent
            else:
                compact = indent is None
            output = format_json(data, compact, indent)
            if ctx.color and click._termui_impl.isatty(sys.stdout):
                output = highlighter(output)
            click.echo(output)
    except KeyboardInterrupt:
        sys.exit(0)


@click.command()
@argument('jsonfile', type=click.Path(readable=True), required=False)
@option('-n', '--nocolor', is_flag=True, help='Disable syntax highlighting')
@version_option(version='0.0', prog_name='JSON Color')
@click.pass_context
def main(ctx, **kwds):
    """JSON text coloring."""
    ctx.color = False if kwds['nocolor'] else True

    if not kwds['jsonfile']:
        if click._termui_impl.isatty(sys.stdin):
            click.echo(ctx.get_usage())
            click.echo('Try `jsoncolor --help` for more information.')
            sys.exit(0)

    data = load_json(ctx, kwds['jsonfile'])

    output(data, ctx, indent=2)
