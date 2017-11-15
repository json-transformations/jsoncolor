"""fixtures and constansts used for test modules."""

import pytest

import jsonconfig

##############################################################################
# CONSTANTS
##############################################################################

DEFAULT = {'default': 's1', 'styles': {'s1': 't1', 's2': 't2'}}


##############################################################################
# FIXTURES
##############################################################################

class ConfigMock:
    """Mock class to return instead of jsonconfig.Config."""
    data = DEFAULT
    filename = '/default/path'
    kwargs = {'dump': {'indent': 4}}


@pytest.fixture()
def cfg_mock(monkeypatch):
    """Patches the context manager call `with jsonconfig.Config...`."""
    def enter(param1):
        return ConfigMock()

    def exit(param1, param2, param3, param4):
        pass

    monkeypatch.setattr(jsonconfig.Config, '__enter__', enter)
    monkeypatch.setattr(jsonconfig.Config, '__exit__', exit)
