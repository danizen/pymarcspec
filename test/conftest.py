import pytest

from marcspec.parser import MarcSpecParser


@pytest.fixture()
def marcspec_parser():
    return MarcSpecParser(parseinfo=True, whitespace='')
