"""jsoncolor.config.py tests"""

import pytest

from jsoncolor.config import config_profile


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
