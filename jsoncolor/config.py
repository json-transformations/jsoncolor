"""Module to configure jsoncolor."""

import sys

import jsonconfig

CONFIG = {
    "default": "solarized",

    "styles": {
        "solarized": {
            "Token": "#8a8a8a",
            "Keyword": "#ffb0ff",
            "Name_Tag": "#2e8ee4",
            "String": "#af8700",
            "Number": "#00afaf",
        },
    },
    "color_code_source": "http://www.colorhexa.com/"
}


def config_profile():
    """Create config file for jsoncolor and set default color scheme."""
    with jsonconfig.Config('jsoncolor') as cfg:
        cfg.data = CONFIG
        cfg.kwargs['dump']['indent'] = 4
        print('JSON Color configuration file created: ' + cfg.filename,
              file=sys.stderr)


def get_color_style(all_colors=False):
    """
    Gets color style from jsoncolor config file.

    Args:
        all_colors (boolean): return singleton value of all values

    Returns:
        default color scheme if all_colors=False
        dict of all preset colors if all_colors=True
    """
    with jsonconfig.Config('jsoncolor', 'r') as cfg:
        colors = cfg.data
    if not all_colors:
        return colors['styles'][colors['default']]
    else:
        return colors['styles']
