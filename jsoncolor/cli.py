"""Command-Line Interface."""

import sys

import click
import click._termui_impl
from click import argument
from click import option
from click import version_option

from jsoncore.cli import optional_jsonfile
from jsonconfig import Config

from jsoncolor.core import create_style_class
from jsoncolor.core import format_json
from jsoncolor.core import get_color_style
from jsoncolor.core import highlighter


SAMPLE = {
    'Style': '',
    'Number': 1,
    'Keyword': True,
    'Array': [
        {
            'Number': 2,
            'Keyword': None,
            'String': 'This is a string!',
        },
    ],
}


def output(data, ctx, indent, style=None):
    """Output data to stdout."""
    try:
        if data:
            if click._termui_impl.isatty(sys.stdin):
                compact = False
                indent = 2 if indent is None else indent
            else:
                compact = indent is None
            output = format_json(data, compact, indent)
            if ctx.color and click._termui_impl.isatty(sys.stdout):
                if style is None:
                    output = highlighter(output)
                else:
                    output = highlighter(output, create_style_class(style))
            click.echo(output)
    except KeyboardInterrupt:
        sys.exit(0)


def sample_styles(ctx):
    """Print SAMPLE in all available preset color styles."""
    styles = get_color_style(all_colors=True)
    for style in styles:
        SAMPLE['Style'] = style
        output(SAMPLE, ctx, indent=2, style=styles[style])


def set_default(style):
    """Set default color style and save to config file."""
    styles = get_color_style(all_colors=True)
    if style not in styles.keys():
        click.echo('[***] ' + style + ' NOT FOUND!\nAvailable Styles:')
        for style in styles.keys():
            click.echo('\t' + style)
        sys.exit(0)

    with Config('jsoncolor', 'r+') as cfg:
        cfg.data['default'] = style
        cfg.kwargs['dump']['indent'] = 4
    click.echo('Default style set to: ' + style)


def create_style():
    """Print how to create a new color style."""
    with Config('jsoncolor', 'r') as cfg:
        path = cfg.filename
    click.echo('To create a new color style, edit the configuration file')
    click.echo('in the following path:')
    click.echo('\n' + path + '\n')


@click.command(name='jsoncolor')
@option('-c', '--create', is_flag=True, help='Create a new color style')
@option('-d', '--default', 'default', help='Set default color style')
@option('-n', '--nocolor', is_flag=True, help='Disable syntax highlighting')
@option('-s', '--styles', is_flag=True, help='Print all preset styles')
@version_option(version='0.2', prog_name='JSON Color')
@optional_jsonfile
@click.pass_context
def main(ctx, **kwds):
    """JSON text coloring."""
    if not any(kwds.values()):
        click.echo('Try `jsoncolor --help` for usage information.')
        sys.exit(0)

    ctx.color = False if kwds['nocolor'] else True

    if kwds['styles']:
        sample_styles(ctx)
        sys.exit(0)

    if kwds['default']:
        set_default(kwds['default'])

    if kwds['create']:
        create_style()
        sys.exit(0)

    output(kwds['jsonfile'], ctx, indent=2)
