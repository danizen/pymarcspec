"""
Logic to search a pymarc.Record based on a compiled MarcSpec AST or object
"""
import sys
from pathlib import Path

from pymarc import MARCReader, Record
from .parser import MarcSpecParser
from .semantics import MarcSearchSemantics


# memoize compiling of strings into AST using some searcher
class MarcSearch:
    def __init__(self):
        self.parser = MarcSpecParser(
            whitespace='',
            semantics=MarcSearchSemantics()
        )
        self.specs = dict()

    def add(self, marcspec):
        spec = self.specs.get(marcspec)
        if spec is None:
            self.specs[marcspec] = spec = self.parser.parse(marcspec)
        return spec

    def search(self, record, marcspec, totext=True):
        spec = self.add(marcspec)
        return spec.search(record, totext=totext)


def marc_search(marcspec, *args):
    search = MarcSearch()
    for path in args:
        if isinstance(path, str):
            path = Path(path)
        if not isinstance(path, Path):
            raise ValueError('path should string or pathlib.Path')
        if not path.exists():
            print(f'{path}: not found')
        else:
            with path.open('rb') as f:
                for record in MARCReader(f):
                    result = search.search(record, marcspec, True)
                    print(result)

if __name__ == '__main__':
    marc_search(*sys.argv[1:])