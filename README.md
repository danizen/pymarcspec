# pymarcspec

## Summary 

An implementation of [MarcSpec](https://github.com/MarcSpec/MarcSpec)
on top of [pymarc](https://gitlab.com/pymarc/pymarc) for searching
MARC records.

## Usage

The idea is to easily use strings to search over MARC without writing complicated
code to handle data.

```python
import sys
from marcspec import MarcSearch
from pymarc import MARCReader

search = MarcSpecSearch()

with open(sys.argv[1], 'rb') as f:
    for record in MARCReader(f):
        mesh_subjects = search.search(record, '650$a{^1=\\2')
        for subfield in mesh_subjects:
            print(subfield.value())
```

## Development

### Building the Parser

To build the parser, run:

```bash
python -m tatsu -o marcparser/parser.py marcparser/marcparser.ebnf
```

### Testing for freshness

The test in `test/test_ebnf.py` compiles the parser from the EBNF into a temporary path, which makes sure
that coffee driven programmers like me remember to compile the parser and check in the changes.



