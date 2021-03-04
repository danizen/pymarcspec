"""
Logic to search a pymarc.Record based on a compiled MarcSpec AST or object
"""
import sys
from argparse import ArgumentParser, FileType

from pymarc import MARCReader, parse_xml_to_array
from .parser import MarcSpecParser
from .semantics import MarcSearchSemantics


class MarcSearchParser(MarcSpecParser):
    def __init__(self, *args, **kwargs):
        kwargs.update({
            'whitespace': '',
            'semantics': MarcSearchSemantics()
        })
        super().__init__(*args, **kwargs)
        self.memoized = dict()


# memoize compiling of strings into specs
class MarcSearch:
    """
    Memoizes compiled specifications to offset
    cost of compiling each again and again.

    Can be used over multiple records and
    multiple specs.
    """
    def __init__(self):
        self.parser = MarcSearchParser()
        self.specs = dict()

    def parse(self, spec):
        compiled_spec = self.specs.get(spec)
        if compiled_spec is None:
            self.specs[spec] = compiled_spec = self.parser.parse(spec)
        return compiled_spec

    def search(self, spec, record, **kwargs):
        compiled_spec = self.parse(spec)
        return compiled_spec.search(record, **kwargs)


def marc_search(marcspec, stream, field_delimiter=':', subfield_delimiter=''):
    searcher = MarcSearch()
    searcher.parse(marcspec)

    if stream.name.endswith('.xml'):
        generator = parse_xml_to_array(stream)
    else:
        generator = MARCReader(stream)
    for record in generator:
        result = searcher.search(
            marcspec, record,
            field_delimiter=field_delimiter,
            subfield_delimiter=subfield_delimiter
        )
        print(result)


def main(args=None):
    if args is None:
        args = sys.argv
    parser = ArgumentParser(prog=args[0], description='Search over Marc records')
    parser.add_argument('marcspec', metavar='EXPR', help='Search expression')
    parser.add_argument('stream', metavar='PATH', type=FileType('rb'))
    parser.add_argument('--field-delimiter', '-f', metavar='CHAR', default=':',
                        help='Delimiter for fields in results')
    parser.add_argument('--subfield-delimiter', '-s', metavar='CHAR', default=',',
                        help='Delimiter for subfields in results')
    opts = parser.parse_args(args[1:])
    marc_search(opts.marcspec, opts.stream,
                opts.field_delimiter, opts.subfield_delimiter)


if __name__ == '__main__':
    main()
