from marcspec.model import (
    MarcSpec,
    FieldSpec,
    IndicatorSpec,
    SubfieldSpec,
    ConditionExpr,
    ConditionTerm,
)


def test_simple_field(search_parser):
    spec = search_parser.parse('880')
    assert spec.type == MarcSpec.FIELD
    assert isinstance(spec.value, FieldSpec)
    assert spec.value.tag == '880'
    assert spec.value.index is None
    assert spec.value.cspec is None
    assert spec.condition is None


def test_simple_indicator(search_parser):
    spec = search_parser.parse('650^2')
    assert spec.type == MarcSpec.INDICATOR
    assert isinstance(spec.value, IndicatorSpec)
    assert spec.value.tag == '650'
    assert spec.value.index is None
    assert spec.condition is None


def test_field_with_cspec_and_conditions(search_parser):
    spec = search_parser.parse('008[0]/0-7{LDR/5!=\\d}')
    assert spec.type == MarcSpec.FIELD
    assert isinstance(spec.value, FieldSpec)
    assert spec.value.tag == '008'
    assert spec.value.index.start == 0
    assert spec.value.index.end is None
    assert spec.value.cspec.start == 0
    assert spec.value.cspec.end == 7
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 1
    term = spec.condition.all[0].any[0]
    assert isinstance(term, ConditionTerm)


def test_indicator_with_conditions(search_parser):
    spec = search_parser.parse('650^2{$a~\\Interstitial}')
    assert spec.type == MarcSpec.INDICATOR
    assert isinstance(spec.value, IndicatorSpec)
    assert spec.value.tag == '650'
    assert spec.value.index is None
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 1
    term = spec.condition.all[0].any[0]
    assert isinstance(term, ConditionTerm)


def test_simple_subfield(search_parser):
    spec = search_parser.parse('245$a-c')
    assert spec.type == MarcSpec.VARDATA
    assert isinstance(spec.value, SubfieldSpec)
    assert spec.value.tag == '245'
    assert len(spec.value.subfields) == 1
    assert spec.value.subfields[0].start == 'a'
    assert spec.value.subfields[0].end == 'c'
    assert spec.value.subfields[0].cspec is None
    assert spec.value.subfields[0].index is None
    assert spec.condition is None


def test_subfield_with_subspec_terms(search_parser):
    spec = search_parser.parse('245$a-c{^1=\\1|?$9}')
    assert spec.type == MarcSpec.VARDATA
    assert isinstance(spec.value, SubfieldSpec)
    assert spec.value.tag == '245'
    assert len(spec.value.subfields) == 1
    assert spec.value.subfields[0].start == 'a'
    assert spec.value.subfields[0].end == 'c'
    assert spec.value.subfields[0].cspec is None
    assert spec.value.subfields[0].index is None
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 2
    terms = spec.condition.all[0].any
    assert isinstance(terms[0], ConditionTerm)
    assert isinstance(terms[1], ConditionTerm)


def test_subfield_many_with_subspec_chain(search_parser):
    spec = search_parser.parse('245$a-c$e$g{^1=\\1}{?$9}')
    assert spec.type == MarcSpec.VARDATA
    assert isinstance(spec.value, SubfieldSpec)
    assert spec.value.tag == '245'
    assert len(spec.value.subfields) == 3
    assert spec.value.subfields[0].start == 'a'
    assert spec.value.subfields[0].end == 'c'
    assert spec.value.subfields[1].start == 'e'
    assert spec.value.subfields[1].end is None
    assert spec.value.subfields[2].start == 'g'
    assert spec.value.subfields[2].end is None

    for subf in spec.value.subfields:
        assert subf.cspec is None
        assert subf.index is None

    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 2
    assert len(spec.condition.all[0].any) == 1
    assert len(spec.condition.all[1].any) == 1
