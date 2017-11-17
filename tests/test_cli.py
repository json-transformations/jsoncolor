"""jsoncolor.cli tests"""

from unittest.mock import patch, call

import pytest

import click._termui_impl
from click import Context
from click.testing import CliRunner

import jsoncolor.cli
from jsoncolor.cli import create_style
from jsoncolor.cli import main
from jsoncolor.cli import output
from jsoncolor.cli import sample_styles
from jsoncolor.cli import set_default
from jsoncolor.cli import SAMPLE


class ClickConfig:
    """Used to pass ctx for click applications."""
    def __init__(self):
        self.color = True


##############################################################################
# TESTS: create_style()
##############################################################################

def test_create_style(cfg_mock, capsys):
    """
    GIVEN a desire to create a new color style
    WHEN the user calls the cli with the -c option
    THEN assert the correct output is printed
    """
    create_style()
    out, err = capsys.readouterr()
    assert out == ('To create a new color style, edit the configuration'
                   ' file\nin the following path:\n\n/default/path\n\n')
    assert err == ''


##############################################################################
# TESTS: main()
##############################################################################

def test_main_no_jsonfile(monkeypatch):
    """
    GIVEN a call to jsoncolor
    WHEN no json file is given
    THEN assert the usage information is properly printed and SystemExit
        is raised
    """
    ctx = Context(main, obj=ClickConfig())
    ctx.command.name = 'jsoncolor'

    monkeypatch.setattr(click._termui_impl, 'isatty', lambda x: True)

    runner = CliRunner()

    result = runner.invoke(main)
    expected_output = ('Usage: jsoncolor [OPTIONS] [JSONFILE]\n'
                       'Try `jsoncolor --help` for more information.\n')

    assert result.output == expected_output


@patch('jsoncolor.cli.output')
@patch('jsoncolor.cli.load_json')
def test_main_jsonfile(lj_mk, o_mk):
    """
    GIVEN a call to jsoncolor
    WHEN a json file is given
    THEN assert load_json() and output() are called
    """
    runner = CliRunner()
    result = runner.invoke(main, ['json_file'])
    assert lj_mk.call_count == 1
    assert o_mk.call_count == 1


@patch('jsoncolor.cli.sample_styles')
def test_main_stylesSet(style_mock):
    """
    GIVEN a call to jsoncolor
    WHEN the -s option is used
    THEN assert sample_styles is called
    """
    runner = CliRunner()
    result = runner.invoke(main, ['-s'])
    assert style_mock.call_count == 1


@patch('jsoncolor.cli.output')
@patch('jsoncolor.cli.load_json')
@patch('jsoncolor.cli.set_default')
def test_main_setDefault(def_mk, lj_mk, o_mk):
    """
    GIVEN a call to jsoncolor
    WHEN the -d option is used
    THEN assert set_default() is called and other required functions called
    """
    runner = CliRunner()
    result = runner.invoke(main, ['-d', 'solarized'])
    def_mk.assert_called_once_with('solarized')
    assert lj_mk.call_count == 1
    assert o_mk.call_count == 1


@patch('jsoncolor.cli.create_style')
def test_main_create(create_mk):
    """
    GIVEN a call to jsoncolor
    WHEN the -c option is used
    THEN assert create_style() is called
    """
    runner = CliRunner()
    result = runner.invoke(main, ['-c'])
    assert create_mk.call_count == 1


##############################################################################
# TESTS: output()
##############################################################################

@pytest.fixture()
def out_fix(patch_tty=True):
    """Sset up args for jsoncolor.cli.output() calls."""
    data = {'k1': 'v1', 'k2': 'v2'}
    ctx = ClickConfig()
    return data, ctx


@pytest.fixture()
def tty_fix(monkeypatch):
    """monkeypatch sys.stdin.isatty for jsoncolor.cli.output() calls."""
    monkeypatch.setattr(click._termui_impl, 'isatty', lambda x: True)
    yield


@patch('jsoncolor.cli.format_json')
@patch('jsoncolor.cli.highlighter')
@patch('click.echo')
def test_output_expectedArgs_styleNone_ttyTrue(e_mk, h_mk, f_mk,
                                               out_fix, tty_fix):
    """
    GIVEN json data to print
    WHEN output is called with the expected args and style=None
    THEN assert the proper functions are called
    """
    data, ctx = out_fix
    f_mk.return_value = data
    h_mk.return_value = data

    output(data, ctx, indent=3, style=None)

    f_mk.assert_called_once_with(data, False, 3)
    h_mk.assert_called_once_with(data)
    e_mk.assert_called_once_with(data)


@patch('jsoncolor.cli.format_json')
@patch('jsoncolor.cli.highlighter')
@patch('jsoncolor.cli.create_style_class')
@patch('click.echo')
def test_output_expectedArgs_styleSet_ttyTrue(e_mk, c_mk, h_mk, f_mk,
                                              out_fix, tty_fix):
    """
    GIVEN json data to print
    WHEN output is called with the expected args and style is set
    THEN assert the proper functions are called
    """
    data, ctx = out_fix
    style = {'style'}
    f_mk.return_value = data
    h_mk.return_value = data
    c_mk.return_value = style

    output(data, ctx, indent=3, style=style)

    f_mk.assert_called_once_with(data, False, 3)
    c_mk.assert_called_once_with(style)
    h_mk.assert_called_once_with(data, style)
    e_mk.assert_called_once_with(data)


@patch('jsoncolor.cli.format_json')
@patch('click.echo')
def test_output_expectedArgs_styleNone_ttyFalse_indentSet(e_mk, f_mk,
                                                          out_fix):
    """
    GIVEN json data to print and invoked from other than a tty
    WHEN output is called with style=None and indent=3
    THEN assert the proper functions are called
    """
    data, ctx = out_fix
    f_mk.return_value = data
    output(data, ctx, indent=3, style=None)
    f_mk.assert_called_once_with(data, False, 3)


@patch('jsoncolor.cli.format_json')
@patch('click.echo')
def test_output_expectedArgs_styleNone_ttyFalse_indentNone(e_mk, f_mk,
                                                           out_fix):
    """
    GIVEN json data to print and invoked from other than a tty
    WHEN output is called with style=None and indent=None
    THEN assert the proper functions are called
    """
    data, ctx = out_fix
    f_mk.return_value = data
    output(data, ctx, indent=None, style=None)
    f_mk.assert_called_once_with(data, True, None)


##############################################################################
# TESTS: sample_styles()
##############################################################################

@patch('jsoncolor.cli.output')
@patch('jsoncolor.cli.get_color_style')
def test_sample_styles(style_mock, output_mock):
    """
    GIVEN a configuration file with multiple styles defined
    WHEN the user calls the cli with the -s option
    THEN assert the output is called with the listed styles
    """
    ctx = ClickConfig()
    style_mock.return_value = {'s1': 't1'}
    sample_styles(ctx)
    assert SAMPLE['Style'] == 's1'
    style_mock.assert_called_once_with(all_colors=True)
    output_mock.assert_called_once_with(SAMPLE, ctx, indent=2, style='t1')


##############################################################################
# TESTS: set_default()
##############################################################################

@patch('click.echo')
@patch('jsoncolor.cli.get_color_style')
def test_set_default_styles_found(style_mock, echo_mock, cfg_mock):
    """
    GIVEN valid default color styles exist
    WHEN a user requests to set the default style to one of the valid styles
    THEN assert the correct style is set and the correct output is printed
    """
    style_mock.return_value = {'s1': 't1', 's2': 't2'}
    set_default('s1')
    style_mock.assert_called_once_with(all_colors=True)
    echo_mock.assert_called_once_with('Default style set to: s1')


@patch('click.echo')
@patch('jsoncolor.cli.get_color_style')
def test_set_default_styles_Notfound(style_mock, echo_mock, cfg_mock):
    """
    GIVEN valid default color styles exist
    WHEN a user requests to set the default style to an style that does not
        exist
    THEN assert SystemExit is raised and the correct output is printed
    """
    with pytest.raises(SystemExit) as sysexc:
        style_mock.return_value = {'s1': 't1', 's2': 't2'}
        set_default('s3')
        style_mock.assert_called_once_with(all_colors=True)
        calls = [call('[***] s3 NOT FOUND!\nAvailable Styles:'), call('\ts1'),
                 call('\ts2')]
        echo_mock.assert_has_calls(calls)
        assert sysexc.type == SystemExit
        assert sysexc.value.code == 0
