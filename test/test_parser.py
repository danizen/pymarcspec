import pytest

from tatsu.exceptions import FailedParse


def test_fieldspec_tag(rawparser):
    ast = rawparser.parse('856')
    assert ast.field.tag == '856'
    assert ast.field.index is None
    assert ast.field.cspec is None
    assert ast.field.subspec is None
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_wildtag(rawparser):
    ast = rawparser.parse('26.')
    assert ast.field.tag == '26.'
    assert ast.field.index is None
    assert ast.field.cspec is None
    assert ast.field.subspec is None
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_spec_range(rawparser):
    ast = rawparser.parse('005/0-7')
    assert ast.field.tag == '005'
    assert ast.field.cspec[1].range.start == '0'
    assert ast.field.cspec[1].range.end == '7'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_spec_pos(rawparser):
    ast = rawparser.parse('005/1')
    assert ast.field.tag == '005'
    assert ast.field.cspec[1].pos == '1'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_index_pos(rawparser):
    ast = rawparser.parse('245[0]')
    assert ast.field.tag == '245'
    assert ast.field.index[1].pos == '0'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_index_range(rawparser):
    ast = rawparser.parse('880[1-4]')
    assert ast.field.tag == '880'
    assert ast.field.index[1].range.start == '1'
    assert ast.field.index[1].range.end == '4'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_subspec_abr(rawparser):
    ast = rawparser.parse('880/1-4{/0=\\2}')
    assert ast.field.tag == '880'
    assert ast.field.cspec[1].range.start == '1'
    assert ast.field.cspec[1].range.end == '4'
    assert len(ast.subspec[0].terms) == 1

    term = ast.subspec[0].terms[0]
    assert term.left.abr.field.cspec[1].pos == '0'
    assert term.op == '='


def test_inds_spec(rawparser):
    ast = rawparser.parse('264^1')
    assert ast.inds.tag == '264'
    assert ast.inds.ind == '1'
    assert ast.field is None
    assert ast.data is None


def test_inds_spec_index(rawparser):
    ast = rawparser.parse('264[0]^1')
    assert ast.inds.index[1].pos == '0'
    assert ast.inds.tag == '264'
    assert ast.inds.ind == '1'
    assert ast.field is None
    assert ast.data is None


def test_subfield_simple(rawparser):
    ast = rawparser.parse('264$a')
    assert ast.data[0].tag == '264'
    assert ast.data[0].codes.code.code== 'a'
    assert ast.data[0].index is None
    assert ast.data[1] == []
    assert ast.data[2] == []
    assert ast.field is None
    assert ast.inds is None


def test_subfield_index_pos_multi(rawparser):
    ast = rawparser.parse('264[0]$a$b$c')
    assert ast.data[0].tag == '264'
    assert ast.data[0].index[1].pos == '0'
    assert ast.data[0].codes.code.code == 'a'
    assert ast.data[1] == []
    assert len(ast.data[2]) == 2
    assert ast.data[2][0][0].code.code == 'b'
    assert ast.data[2][1][0].code.code == 'c'
    assert ast.field is None
    assert ast.inds is None


def test_subfield_range(rawparser):
    ast = rawparser.parse('264$b-d')
    assert ast.data[0].tag == '264'
    assert ast.data[0].index is None
    assert ast.data[0].codes.range.start == 'b'
    assert ast.data[0].codes.range.end == 'd'
    assert ast.data[1] == []
    assert ast.data[2] == []
    assert ast.field is None
    assert ast.inds is None


def test_subfield_with_subspec_field(rawparser):
    ast = rawparser.parse('650$a{650^2=\\toolong}')
    assert ast.field is None
    assert ast.inds is None
    assert ast.data[0].tag == '650'
    assert ast.data[0].codes.code.code == 'a'
    assert ast.data[2] == []
    assert len(ast.data[1][0].terms) == 1

    term = ast.data[1][0].terms[0]
    assert term.op == '='
    assert term.left.inds.tag == '650'
    assert term.left.inds.ind == '2'
    assert term.right.cmp[1] == 'toolong'


def test_subfield_with_subspec_subfieldabbr_biop(rawparser):
    ast = rawparser.parse('650$a{$9=$8}')
    assert ast.field is None
    assert ast.inds is None
    assert ast.data[0].tag == '650'
    assert ast.data[0].codes.code.code == 'a'
    assert ast.data[2] == []
    assert len(ast.data[1][0].terms) == 1

    term = ast.data[1][0].terms[0]
    assert term.op == '='
    assert term.left.abr.data.code.code == '9'
    assert term.right.abr.data.code.code == '8'


def test_subfield_with_subspec_subfield_unop(rawparser):
    ast = rawparser.parse('020$c{?020$a}')
    assert ast.field is None
    assert ast.inds is None
    assert ast.data[0].tag == '020'
    assert ast.data[0].codes.code.code == 'c'
    assert ast.data[2] == []
    assert len(ast.data[1][0].terms) == 1

    term = ast.data[1][0].terms[0]
    assert term.op == '?'
    assert term.left is None
    assert term.right.data.tag == '020'
    assert term.right.data.codes.code.code == 'a'
    assert term.right.field is None
    assert term.right.inds is None


@pytest.mark.parametrize('pattern', [
    'LDR',              # match the leader
    '00.',              # match all control fields
    '7..',              # match all 7xx fields
    '100',              # match specifically the datafields with tag==100
    'LDR/0-4',          # first five characters of the leader
    'LDR/6',            # The 7th character from the level (0-based)
    '007/0',            # 1st character from 007 control field
    '007/1-#',          # all characters but first in the 007
    '007/#',            # last character in the 007 field
    '245$a',            # Each $a subfield of each 245
    '245$a/#-1',        # last 2 characters of each 245$a
    '245$a$b$c',        # each subfield $a, $b, and $c of each 245
    '245$a-c',          # subfields $a through $c of each 245
    '245$a-c$e-f',
    '300[0]',           # 1st occurrence of 300
    '300[1]',           # 2nd occurrence of 300
    '300[0-2]',         # 1st, 2nd, and 3rd occurrence of 300
    '300[1-#]',         # All but the first 300
    '300[#]',           # last occurrence of 300
    '300[#-1]',         # last and penultimate 300
    '300[0]$a',         # each subfield $a of 1st 300
    '300$a[0]',         # first subfield $a of each 300
    '300$a[#]',         # last subfield $a of each 300
    '300$a[#-1]',       # last two subfield $a of each 300
    '880^1',            # indicator 1 of each 880
    '880[1]^2',         # indicator 2 of the 2nd 880
    # subspec
    '020$c{?020$a}',    # each subfield $c of each 020, if any subfield $a of any 020 exists
    '020$z{!020$a}',
    '008/18{LDR/6=\\t}',
    '245$b{007/0=\\a|007/0=\\t}',       # multiple terms
    '008/18{LDR/6=\\a}{LDR/7=\\a|LDR/7=\\c|LDR/7=\\d|LDR/7=\\m}',
    '880$a{100$6~$6/3-5}{100$6~\\880}',     # chaining
    # abbreviations in subspecs
    '007[1]/3{/0=\\v}',
    '020$c{$a}',
    '800[0]{$a~\\Poe}{^2=\\1}',
    '245$a{/0-2=\\The}',
    '020$c{$q=\\paperback}',
])
def test_parser_accepts(pattern, rawparser):
    ast = rawparser.parse(pattern)
    assert ast.parseinfo.rule == 'marcSpec'


@pytest.mark.parametrize('pattern', [
    '880[0-',
    '245[',
    '22',
    '300[ 0]',
    '300[0 ]',
    '300 [0-2]',
    '300[0 -2]',
    '300[0- 2]',
    '300[0-2 ]',
    '007 /#',
    '007/ #',
    '007/0- 1',
    '007/0 -1',
    '020$c{ ?$a}'
    '020$c {$a}',
    '020$c{$ a}',
    '020$c{$a }',
])
def test_parser_rejects(pattern, rawparser):
    with pytest.raises(FailedParse) as info:
        rawparser.parse(pattern)
    print(info.value)
