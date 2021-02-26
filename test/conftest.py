import pytest

from marcspec.parser import MarcSpecParser
from marcspec.semantics import MarcSearchSemantics


@pytest.fixture()
def rawparser():
    return MarcSpecParser(parseinfo=True, whitespace='')


@pytest.fixture()
def search_parser():
    return MarcSpecParser(whitespace='', semantics=MarcSearchSemantics())
