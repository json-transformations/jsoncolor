"""jsoncolor.core tests"""

from unittest.mock import patch

import pytest
import pygments.style

from jsoncolor.core import validate_style
from jsoncolor.core import create_style_class
from jsoncolor.core import format_json
from jsoncolor.core import highlighter

##############################################################################
# CONSTANTS
##############################################################################

DATA = {'a': 'b', 'c': 'd'}

STYLE_TEST = {'Token': '#8a8a8a', 'Keyword': '#af0000', 'Name_Tag': '#268bd2',
              'String': '#af8700', 'Number': '#00afaf'}


##############################################################################
# TESTS: validate_style()
##############################################################################

def test_validate_style_give_good_style():
    """
    GIVEN a style dict with known-good color values
    WHEN validating the colors values
    THEN assert the entire original dict is returned
    """
    style = validate_style(STYLE_TEST)
    assert style == STYLE_TEST


def test_validate_style_give_bad_style():
    """
    GIVEN a style dict with some known-bad color values
    WHEN validating the colors values
    THEN assert a dict is returned with invalid values returned
    """
    STYLE_TEST['Token'] = '8a8a8a'
    STYLE_TEST['Keyword'] = '!af0000'
    STYLE_TEST['Name_Tag'] = '#268bdx'
    style = validate_style(STYLE_TEST)
    assert style == {'String': '#af8700', 'Number': '#00afaf'}


##############################################################################
# TESTS: create_style_class()
##############################################################################

def test_create_style_class():
    """
    GIVEN a color style as a dict with all required key-value pairs
    WHEN creating a pygments.style.Style class with the given style
    THEN assert the class is properly created
    """
    style = create_style_class(STYLE_TEST)
    assert hasattr(style, 'styles')
    assert style.__class__ == pygments.style.StyleMeta


##############################################################################
# TESTS: format_json()
##############################################################################

testargs = [
    (False, 2, None),
    (False, 4, None),
    (True, 2, (',', ':')),
    (True, 4, (',', ':')),
]


@pytest.mark.parametrize('comp,ind,sep', testargs)
@patch('json.dumps')
def test_format_json_defaults(dumps_mock, comp, ind, sep):
    """
    GIVEN a dict
    WHEN converting to json
    THEN assert json.dumps is called with correct args
    """
    format_json(STYLE_TEST, compact=comp, indent=ind)
    dumps_mock.assert_called_once_with(STYLE_TEST, separators=sep, indent=ind)


##############################################################################
# TESTS: highlighter()
##############################################################################

@patch('jsoncolor.core.Terminal256Formatter')
@patch('pygments.highlight')
@patch('jsoncolor.core.JsonLexer')
def test_highlighter(json_mock, highl_mock, term256_mock):
    """
    GIVEN json content to highlight
    WHEN highligher() is called with the json and color-style
    THEN assert the appropriate pygments classes/functions are used
    """
    highlighter(DATA, STYLE_TEST)
    highl_mock.assert_called_once()
    json_mock.assert_called_once()
    term256_mock.assert_called_once()


def test_higlighter_exception():
    """
    GIVEN json content to highlight
    WHEN highlighter is called with an a color style not of the
        pygments.style.Style class
    THEN assert ValueError is thrown and the original data is returned
        unhighlighted
    """
    h = highlighter(DATA, STYLE_TEST)
    assert h == DATA
