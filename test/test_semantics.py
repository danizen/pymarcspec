from pymarcspec.model import (
    FieldFilter,
    IndicatorFilter,
    ConditionExpr,
    ConditionTerm,
)


def test_simple_field(search_parser):
    spec = search_parser.parse('880')
    assert isinstance(spec.filter, FieldFilter)
    assert spec.tag == '880'
    assert spec.filter.index is None
    assert spec.filter.cspec is None
    assert spec.condition is None


def test_simple_indicator(search_parser):
    spec = search_parser.parse('650^2')
    assert isinstance(spec.filter, IndicatorFilter)
    assert spec.tag == '650'
    assert spec.filter.index is None
    assert spec.condition is None


def test_field_with_cspec_and_conditions(search_parser):
    spec = search_parser.parse('008[0]/0-7{LDR/5!=\\d}')
    assert isinstance(spec.filter, FieldFilter)
    assert spec.tag == '008'
    assert spec.filter.index.start == 0
    assert spec.filter.index.end is None
    assert spec.filter.cspec.start == 0
    assert spec.filter.cspec.end == 7
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 1
    term = spec.condition.all[0].any[0]
    assert isinstance(term, ConditionTerm)


def test_indicator_with_conditions(search_parser):
    spec = search_parser.parse('650^2{$a~\\Interstitial}')
    assert isinstance(spec.filter, IndicatorFilter)
    assert spec.tag == '650'
    assert spec.filter.index is None
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 1
    term = spec.condition.all[0].any[0]
    assert isinstance(term, ConditionTerm)


def test_simple_subfield(search_parser):
    spec = search_parser.parse('245$a-c')
    assert isinstance(spec.filter, list)
    assert spec.tag == '245'
    assert len(spec.filter) == 1
    assert spec.filter[0].start == 'a'
    assert spec.filter[0].end == 'c'
    assert spec.filter[0].cspec is None
    assert spec.filter[0].index is None
    assert spec.condition is None


def test_subfield_with_subspec_terms(search_parser):
    spec = search_parser.parse('245$a-c{^1=\\1|?$9}')
    assert isinstance(spec.filter, list)
    assert spec.tag == '245'
    assert len(spec.filter) == 1
    assert spec.filter[0].start == 'a'
    assert spec.filter[0].end == 'c'
    assert spec.filter[0].cspec is None
    assert spec.filter[0].index is None
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 1
    assert len(spec.condition.all[0].any) == 2
    terms = spec.condition.all[0].any
    assert isinstance(terms[0], ConditionTerm)
    assert isinstance(terms[1], ConditionTerm)


def test_subfield_many_with_subspec_chain(search_parser):
    spec = search_parser.parse('245$a-c$e$g{^1=\\1}{?$9}')
    assert isinstance(spec.filter, list)
    assert spec.tag == '245'
    assert len(spec.filter) == 3
    assert spec.filter[0].start == 'a'
    assert spec.filter[0].end == 'c'
    assert spec.filter[1].start == 'e'
    assert spec.filter[1].end is None
    assert spec.filter[2].start == 'g'
    assert spec.filter[2].end is None
    for filter in spec.filter:
        assert filter.cspec is None
        assert filter.index is None
    assert isinstance(spec.condition, ConditionExpr)
    assert len(spec.condition.all) == 2
    assert len(spec.condition.all[0].any) == 1
    assert len(spec.condition.all[1].any) == 1
