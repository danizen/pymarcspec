"""
Logic to search a pymarc.Record based on a compiled MarcSpec AST or object
"""
import sys
from argparse import ArgumentParser, FileType

from pymarc import MARCReader
from .parser import MarcSpecParser
from .semantics import MarcSearchSemantics


# memoize compiling of strings into AST using some searcher
class MarcSearchParser(MarcSpecParser):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'whitespace': '',
            'semantics': MarcSearchSemantics()

        })
        super().__init__(*args, **kwargs)


def marc_search(marcspec, stream, delim='\n'):
    parser = MarcSearchParser()
    spec = parser.parse(marcspec)

    for record in MARCReader(stream):
        result = spec.search(record, totext=True, delim=delim)
        print(result)
        print('')


def main(args=None):
    if args is None:
        args = sys.argv
    parser = ArgumentParser(prog=args[0], description='Search over Marc records')
    parser.add_argument('marcspec', metavar='EXPR', help='Search expression')
    parser.add_argument('stream', metavar='PATH', type=FileType('rb'))
    opts = parser.parse_args(args[1:])
    marc_search(opts.marcspec, opts.stream)


if __name__ == '__main__':
    main()
