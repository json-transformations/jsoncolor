"""
JSON Content Coloring

Functions used to color and highlight JSON content for better viewing on the
command-line.
"""

import json

import pygments
import pygments.style
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import JsonLexer
from jsonconfig import Config


def get_config_color():
    """Gets color scheme from jsoncolor config file."""
    with Config('jsoncolor', 'r') as cfg:
        data = cfg.data
    return data['styles'][data['default']]


STYLE = get_config_color()


def format_json(d, compact=False, indent=2):
    """Format JSON; compact or indented."""
    separators = (',', ':') if compact else None
    return json.dumps(d, indent=indent, separators=separators)


def highlighter(d, style=STYLE):
    """JSON Syntax highlighter."""
    try:
        formatter = Terminal256Formatter(style=StyleClass)
    except (NameError, AttributeError):
        return d
    return pygments.highlight(d, JsonLexer(), formatter)


class StyleClass(pygments.style.Style):
    """
    Create a style to be used by pygments by reading in default color
    style from jsoncolor config file.
    """
    styles = {
        pygments.token.Token: STYLE['Token'],
        pygments.token.Keyword: STYLE['Keyword'],
        pygments.token.Name.Tag: STYLE['Name_Tag'],
        pygments.token.String: STYLE['String'],
        pygments.token.Number: STYLE['Number'],
    }
