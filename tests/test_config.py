"""jsoncolor.config.py tests"""

import pytest

from jsoncolor.config import config_profile
from jsoncolor.config import get_color_style


##############################################################################
# TESTS: config_profile()
##############################################################################

def test_configProfile(cfg_mock, capsys):
    """
    WHEN a new install or reconfiguration is commanded
    THEN assert the config file is properly created
    """
    config_profile()
    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'JSON Color configuration file created: /default/path\n'


##############################################################################
# TESTS: get_color_style()
##############################################################################

def test_get_color_style_all_colors_false(cfg_mock):
    """
    GIVEN an existing jsoncolor config file
    WHEN the default color style is retrieved from the config file
    THEN assert the default style is returned
    """
    style = get_color_style(all_colors=False)
    assert style == 't1'


def test_get_color_style_all_colors_true(cfg_mock):
    """
    GIVEN an existing jsoncolor config file
    WHEN all preset color styles are retrieved from the config file
    THEN assert all styles are properly returned
    """
    styles = get_color_style(all_colors=True)
    assert styles == {'s1': 't1', 's2': 't2'}
