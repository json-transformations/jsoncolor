"""
JSON Text Coloring

Functions used to color and highlight JSON content for better viewing on the
command-line.
"""

import json
from string import hexdigits

import pygments
import pygments.style
from pygments.formatters.terminal256 import Terminal256Formatter
from pygments.lexers import JsonLexer

from jsoncolor.config import CONFIG
from jsoncolor.config import get_color_style


def validate_style(style):
    """
    Validates to see if a given style has valid values.

    Args:
        style (dict): color style dict with values as hexadecimal color
            codes, as found at: http://www.colorhexa.com/

    Returns:
        style (dict): values that are not valid will be deleted and a
            truncated dict will be returned.  All valid values will remain.
    """
    valid = {}
    for k, v in style.items():
        if (v.startswith('#') and all([d in hexdigits for d in v[1:]])):
            valid[k] = v
    return valid


def create_style_class(style=None):
    """
    Create a Style Class.

    Args:
        style (dict): color style dict with keywords:
            Token, Keyword, Name_Tag, String, Number

    Returns:
        StyleClass with appropriate color set for pygments
            Terminal256Formatter
    """
    if style is None:
        style = get_color_style()
    style = validate_style(style)

    class StyleClass(pygments.style.Style):
        styles = {
            pygments.token.Token: style.get('Token',
                CONFIG['styles']['solarized']['Token']),
            pygments.token.Keyword: style.get('Keyword',
                CONFIG['styles']['solarized']['Keyword']),
            pygments.token.Name.Tag: style.get('Name_Tag',
                CONFIG['styles']['solarized']['Name_Tag']),
            pygments.token.String: style.get('String',
                CONFIG['styles']['solarized']['String']),
            pygments.token.Number: style.get('Number',
                CONFIG['styles']['solarized']['Number']),
        }

    return StyleClass


def format_json(data, compact=False, indent=2):
    """
    Format Dict to JSON.

    Args:
        data (dict): python dict
        compact (boolean): non-indended output
        indent (int): set indenting for compact=False mode

    Returns:
        data formatted to json-serialized content
    """
    separators = (',', ':') if compact else None
    return json.dumps(data, indent=indent, separators=separators)


def highlighter(data, style=None):
    """
    JSON Syntax Highlighter.

    Args:
        data (json): json-serialized content
        style (StyleClass): Style to be used by Terminal256Formatter,
            return value from create_style_class()

    Returns:
        Json-serialized content with proper color coding
        Json-serialized content without color coding if a ValueError
            from Terminal256Formatter is thrown.
    """
    if style is None:
        style = create_style_class(get_color_style())
    try:
        formatter = Terminal256Formatter(style=style)
    except (ValueError):
        return data
    return pygments.highlight(data, JsonLexer(), formatter)
