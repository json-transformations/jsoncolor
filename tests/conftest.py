"""fixtures and constansts used for test modules."""

import pytest
import jsonconfig
from click import Context


##############################################################################
# CONSTANTS
##############################################################################

DEFAULT = {'default': 's1', 'styles': {'s1': 't1', 's2': 't2'}}


##############################################################################
# FIXTURES
##############################################################################

class DummyClass:
    """Dummy Class to pass as the command option to click.Context."""
    allow_extra_args = False
    allow_interspersed_args = False
    ignore_unknown_options = False


class ClickConfig(Context):
    """Used to pass ctx for click applications."""
    def __init__(self):
        Context.__init__(self, DummyClass)
        self.color = True

    def __iter__(self):
        for attr in dir(DummyClass):
            yield attr


@pytest.fixture()
def ctx_mock():
    """Returns a mocked click.Context() object."""
    return ClickConfig()


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
