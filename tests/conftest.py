"""fixtures and constansts used for test modules."""

import pytest

from jsonconfig.core import Config

##############################################################################
# CONSTANTS
##############################################################################

DEFAULT = {'default': 's1', 'styles': {'s1': 't1', 's2': 't2'}}


##############################################################################
# FIXTURES
##############################################################################

class ConfigMock:
    """Mock class to return instead of jsonconfig.core.Config."""
    data = DEFAULT
    filename = '/default/path'
    kwargs = {'dump': {'indent': 4}}


@pytest.fixture()
def cfg_mock(monkeypatch):
    """Patches the context manager call `with jsonconfig.core.Config...`."""
    def enter(param1):
        return ConfigMock

    def exit(param1, param2, param3, param4):
        pass

    monkeypatch.setattr(Config, '__enter__', enter)
    monkeypatch.setattr(Config, '__exit__', exit)
