# pymarcspec
[![Build Status](https://travis-ci.org/danizen/pymarcspec.svg?branch=main)](https://travis-ci.org/danizen/pymarcspec) [![Coverage Status](https://coveralls.io/repos/github/danizen/pymarcspec/badge.svg?branch=main)](https://coveralls.io/github/danizen/pymarcspec?branch=main)

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
spec = parser.parse('650$a$0')
with open(sys.argv[1], 'rb') as f:
    for record in MARCReader(f):
        subjects = spec.search(record, field_delimiter=':', subfield_delimiter=',')
        print(subjects)
```

There is also a `MarcSearch` object that memoizes each search expression, so that 
you can conveniently run a number of different searches without creating several
parsed specs. For example:

```python
import csv
import sys
from pymarcspec import MarcSearch
from pymarc import MARCReader

writer = csv.writer(sys.stdout, dialect='unix', quoting=csv.QUOTE_MINIMAL)
writer.writerow(['id', 'title', 'subjects'])

marcsearch = MarcSearch()
with open(sys.argv[1], 'rb') as f:
    for record in MARCReader(f):
        control_id = marcsearch.search('100', record)
        title = marcsearch.search('245[0]$a-c', record)
        subjects = marcsearch.search('650$a', record, field_delimiter=', ')
        writer.writerow([control_id, title, subjects])        
```

## Development

### Building the Parser

To build the parser, run:

```bash
python -m tatsu -o marcparser/parser.py marcparser/marcparser.ebnf
```

Note that this builds a class `MarcSpecParser`, which implements the full specification from
[MarcSpec](https://github.com/MarcSpec/MarcSpec), the `MarcSearchParser` is a subclass
that builds an instance of  `MarcSpec`; building this structure has some 
restrictions for what I needed when I wrote it.

### Testing for freshness

The test in `test/test_ebnf.py` compiles the parser from the EBNF into a temporary path, which makes sure
that coffee driven programmers like me remember to compile the parser and check in the changes.

## Performance

It is not obvious this is needed.  It may be fine for instance to use XPath expressions.
Suppose we are going to do a lot of these conversions - if XPath is fast enough, the work of converting
from a `pymarc.Record` to MARCXML will be amoritized by many searches.  Jupyter Notebooks have a %timeit
magic that allows us to check this:

Let us check the performance of the simplest such XPath expression:

```python
In [34]: %timeit ''.join(doc.xpath('./controlfield[@tag="001"]/text()'))                                                                                  
19.4 µs ± 1.07 µs per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

And compare it to parsing a spec and searching:

```python
In [37]: from pymarcspec import MarcSearchParser                                                    

In [38]: parser = MarcSearchParser()                                                                

In [39]: spec = parser.parse('001')                                                                 

In [40]: spec.search(record)                                                                        
Out[40]: '1589530'

In [41]: %timeit spec.search(record)                                                                
7.89 µs ± 253 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
```

So, from a performance perspective this is clearly a win, and the expression is much closer
to library IT.
