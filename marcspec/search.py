"""
Logic to search a pymarc.Record based on a compiled MarcSpec AST or object
"""
from .parser import MarcSpecParser
from .semantics import MarcSearchSemantics


# memoize compiling of strings into AST using some searcher
class MarcSpecSearch:

    def __init__(self):
        self.parser = MarcSpecParser(semantics=MarcSearchSemantics())
        self.specs = dict()

    def _spec(self, marcspec):
        spec = self.specs.get(marcspec)
        if spec is None:
            self.specs[marcspec] = spec = self.parser.parse(marcspec)
        return spec

    def search(self, record, marcspec):
        spec = self._spec(marcspec)
        if spec.field:
            return self._search_fields(record, spec)
        elif spec.inds:
            return self._search_indicators(record, spec)
        elif spec.data:
            return self._search_data(record, spec)
        else:
            raise RuntimeError('All MarcSpec should search fields, indicators, or variable data')

    def _search_fields(self, record, spec):
        raise RuntimeError('field search is not implemented')

    def _search_indicators(self, record, spec):
        raise RuntimeError('indicator search is not implemented')

    def _search_data(self, record, spec):
        raise RuntimeError('search over variable data is not implemented')
