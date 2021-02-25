def test_fieldspec_tag(marcspec_parser):
    ast = marcspec_parser.parse('856')
    assert ast.field.tag == '856'
    assert ast.field.index is None
    assert ast.field.cspec is None
    assert ast.field.subspec is None
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_wildtag(marcspec_parser):
    ast = marcspec_parser.parse('26.')
    assert ast.field.tag == '26.'
    assert ast.field.index is None
    assert ast.field.cspec is None
    assert ast.field.subspec is None
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_spec_range(marcspec_parser):
    ast = marcspec_parser.parse('005/0-7')
    assert ast.field.tag == '005'
    assert ast.field.cspec[1].range.start == '0'
    assert ast.field.cspec[1].range.end == '7'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_spec_pos(marcspec_parser):
    ast = marcspec_parser.parse('005/1')
    assert ast.field.tag == '005'
    assert ast.field.cspec[1].pos == '1'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_index_pos(marcspec_parser):
    ast = marcspec_parser.parse('245[0]')
    assert ast.field.tag == '245'
    assert ast.field.index[1].pos == '0'
    assert ast.data is None
    assert ast.inds is None


def test_fieldspec_index_range(marcspec_parser):
    ast = marcspec_parser.parse('880[1-4]')
    assert ast.field.tag == '880'
    assert ast.field.index[1].range.start == '1'
    assert ast.field.index[1].range.end == '4'
    assert ast.data is None
    assert ast.inds is None


def test_inds_spec(marcspec_parser):
    ast = marcspec_parser.parse('264^1')
    assert ast.inds.tag == '264'
    assert ast.inds.ind == '1'
    assert ast.field is None
    assert ast.data is None


def test_inds_spec_index(marcspec_parser):
    ast = marcspec_parser.parse('264[0]^1')
    assert ast.inds.index[1].pos == '0'
    assert ast.inds.tag == '264'
    assert ast.inds.ind == '1'
    assert ast.field is None
    assert ast.data is None


def test_subfield_simple(marcspec_parser):
    ast = marcspec_parser.parse('264$a')
    assert ast.data[0].tag == '264'
    assert ast.data[0].codes.code.code== 'a'
    assert ast.data[0].index is None
    assert ast.data[1] == []
    assert ast.data[2] == []
    assert ast.field is None
    assert ast.inds is None


def test_subfield_index_pos_multi(marcspec_parser):
    ast = marcspec_parser.parse('264[0]$a$b$c')
    assert ast.data[0].tag == '264'
    assert ast.data[0].index[1].pos == '0'
    assert ast.data[0].codes.code.code == 'a'
    assert ast.data[1] == []
    assert len(ast.data[2]) == 2
    assert ast.data[2][0][0].code.code == 'b'
    assert ast.data[2][1][0].code.code == 'c'
    assert ast.field is None
    assert ast.inds is None


def test_subfield_range(marcspec_parser):
    ast = marcspec_parser.parse('264$b-d')
    assert ast.data[0].tag == '264'
    assert ast.data[0].index is None
    assert ast.data[0].codes.range.start == 'b'
    assert ast.data[0].codes.range.end == 'd'
    assert ast.data[1] == []
    assert ast.data[2] == []
    assert ast.field is None
    assert ast.inds is None


def test_subfield_with_subspec_field(marcspec_parser):
    ast = marcspec_parser.parse('650$a{650^2=\\toolong}')
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


def test_subfield_with_subspec_subfieldabbr_biop(marcspec_parser):
    ast = marcspec_parser.parse('650$a{$9=$8}')
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


def test_subfield_with_subspec_subfield_unop(marcspec_parser):
    ast = marcspec_parser.parse('020$c{?020$a}')
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
