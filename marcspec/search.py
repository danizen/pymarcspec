"""
Logic to search a pymarc.Record based on a compiled MarcSpec AST or object
"""
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

    def search(self, record, marcspec):
        spec = self.add(marcspec)
        return spec.search(record)
