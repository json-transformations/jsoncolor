"""
JSON Content Coloring

Functions used to color and highlight JSON content for better viewing on the
command-line.
"""

import json
from string import hexdigits

import pygments
import pygments.style
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import JsonLexer
from jsonconfig import Config


def get_color_style(all_colors=False):
    """
    Gets color style from jsoncolor config file.

    Args:
        * all_colors (boolean): return singleton value of all values

    Returns:
        * default color scheme if all_colors=False
        * dict of all preset colors if all_colors=True
    """
    with Config('jsoncolor', 'r') as cfg:
        colors = cfg.data
    if not all_colors:
        return colors['styles'][colors['default']]
    else:
        return colors['styles']


STYLE = get_color_style()


def validate_style(style):
    """
    Validates to see if a given style has valid values.

    Args:
        * style (dict): color style dict with values as hexadecimal color
            codes, as found at: http://www.colorhexa.com/

    Returns:
        * style (dict): values that are not valid will be deleted and a
            truncated dict will be returned.  All valid values will remain.
    """
    valid = {}
    for k, v in style.items():
        if (v.startswith('#') and all([d in hexdigits for d in v[1:]])):
            valid[k] = v
    return valid


def create_style_class(style):
    """
    Create a Style Class.

    Args:
        * style (dict): color style dict with keywords:
            Token, Keyword, Name_Tag, String, Number

    Returns:
        * StyleClass with appropriate color set for pygments
            Terminal256Formatter
    """
    style = validate_style(style)

    class StyleClass(pygments.style.Style):
        styles = {
            pygments.token.Token: style.get('Token', '#8a8a8a'),
            pygments.token.Keyword: style.get('Keyword', '#ffb0ff'),
            pygments.token.Name.Tag: style.get('Name_Tag', '#2e8ee4'),
            pygments.token.String: style.get('String', '#af8700'),
            pygments.token.Number: style.get('Number', '#00afaf'),
        }

    return StyleClass


def format_json(data, compact=False, indent=2):
    """
    Format Dict to JSON.

    Args:
        * data (dict): python dict
        * compact (boolean): non-indended output
        * indent (int): set indenting for compact=False mode

    Returns:
        * data formatted to json-serialized content
    """
    separators = (',', ':') if compact else None
    return json.dumps(data, indent=indent, separators=separators)


def highlighter(data, style=create_style_class(STYLE)):
    """
    JSON Syntax Highlighter.

    Args:
        * data (json): json-serialized content
        * style (StyleClass): Style to be used by Terminal256Formatter,
            return value from create_style_class()

    Returns:
        * Json-serialized content with proper color coding
        * Json-serialized content without color coding if a ValueError
            from Terminal256Formatter is thrown.
    """
    try:
        formatter = Terminal256Formatter(style=style)
    except (ValueError):
        return data
    return pygments.highlight(data, JsonLexer(), formatter)
