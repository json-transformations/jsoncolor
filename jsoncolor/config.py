"""Module to configure jsoncolor."""

import sys

from jsonconfig import Config

CONFIG = {
    "default": "solarized",

    "styles":
        {"solarized": {
            "Token": "#8a8a8a",
            "Keyword": "#ffb0ff",
            "Name_Tag": "#2e8ee4",
            "String": "#af8700",
            "Number": "#00afaf"
        }, },
    "color_code_source": "http://www.colorhexa.com/"
}


def config_profile():
    """Create config file for jsoncolor and set default color scheme."""
    with Config('jsoncolor') as cfg:
        cfg.data = CONFIG
        cfg.kwargs['dump']['indent'] = 4
        print('JSON Color configuration file created: ' + cfg.filename,
              file=sys.stderr)
