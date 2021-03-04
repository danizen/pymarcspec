import os

from pymarc import parse_xml_to_array
import pytest

from pymarcspec.parser import MarcSpecParser
from pymarcspec.semantics import MarcSearchSemantics

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


@pytest.fixture()
def rawparser():
    return MarcSpecParser(parseinfo=True, whitespace='')


@pytest.fixture()
def search_parser():
    return MarcSpecParser(whitespace='', semantics=MarcSearchSemantics())


@pytest.fixture(scope='session')
def jama_path():
    return os.path.join(DATA_DIR, 'nlmui-7501160.xml')


@pytest.fixture(scope='session')
def jama_record(jama_path):
    record, = parse_xml_to_array(jama_path)
    return record
