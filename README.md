# pymarcspec
[![Build Status](https://travis-ci.org/danizen/pymarcspec.svg?branch=master)](https://travis-ci.org/danizen/pymarcspec) [![Coverage Status]

## Summary 

An implementation of [MarcSpec](https://github.com/MarcSpec/MarcSpec)
on top of [pymarc](https://gitlab.com/pymarc/pymarc) for searching
MARC records.

## Usage

The idea is to easily use strings to search over MARC without writing complicated
code to handle data.

```python
import sys
from pymarcspec import MarcSearchParser
from pymarc import MARCReader

parser = MarcSearchParser()
spec = parser.parse('650$a{^1=\\2}')
with open(sys.argv[1], 'rb') as f:
    for record in MARCReader(f):
        mesh_subjects = spec.search(record)
        for subfield in mesh_subjects:
            print(subfield.value())
```

## Development

### Building the Parser

To build the parser, run:

```bash
python -m tatsu -o marcparser/parser.py marcparser/marcparser.ebnf
```

Note that this builds a class MarcSpecParser, which implements the full specification from
[MarcSpec](https://github.com/MarcSpec/MarcSpec), the `MarcSearchParser` is a subclass
that builds an instance of  `MarcSpec`; building this structure has some 
restrictions for what I needed when I wrote it.

### Testing for freshness

The test in `test/test_ebnf.py` compiles the parser from the EBNF into a temporary path, which makes sure
that coffee driven programmers like me remember to compile the parser and check in the changes.



