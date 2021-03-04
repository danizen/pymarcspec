import difflib
import os
import re
import sys

import tatsu

import pymarcspec.parser


def test_compile(tmp_path):
    """
    Test that the BNF file compiles to the same content as the loader.parser
    """
    expected_source_path = pymarcspec.parser.__file__
    grammar_path = re.sub('parser.py$', 'marcspec.ebnf', expected_source_path)
    assert os.path.exists(grammar_path)
    actual_source_path = str(tmp_path / 'test_parser.py')

    with open(grammar_path, 'r', encoding='utf-8') as fp:
        grammar = fp.read()
    print(actual_source_path)
    generated_source = tatsu.to_python_sourcecode(grammar)
    with open(actual_source_path, 'w') as fp:
        fp.write(generated_source)

    with open(expected_source_path) as fp:
        expected_lines = fp.readlines()
    with open(actual_source_path) as fp:
        actual_lines = fp.readlines()
    delta = difflib.unified_diff(
        expected_lines,
        actual_lines,
        fromfile='pymarcspec/parser.py',
        tofile=actual_source_path
    )
    good = True
    for line in delta:
        print(line, file=sys.stderr)
        good = False
    assert good, "There were differences in compiled parser"
