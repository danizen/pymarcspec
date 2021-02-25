# pymarcspec

## Summary 

Implementation of [MarcSpec](https://github.com/MarcSpec/MarcSpec) on top of pymarc.

## Building the Parser

To build the parser, run:

```bash
python -m tatsu -o marcparser/parser.py marcparser/marcparser.ebnf
```

## Testing for freshness

The test in `test/test_ebnf.py` compiles the parser from the EBNF into a temporary path, which makes sure
that coffee driven programmers like me remember to compile the parser and check in the changes.



