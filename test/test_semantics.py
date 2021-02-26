from marcspec.model import (
    MarcSpec,
    FieldSpec,
    IndicatorSpec,
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
    assert spec.conditions is None


def test_simple_indicator(search_parser):
    spec = search_parser.parse('650^2')
    assert spec.type == MarcSpec.INDICATOR
    assert isinstance(spec.value, IndicatorSpec)
    assert spec.value.tag == '650'
    assert spec.value.index is None
    assert spec.conditions is None


def test_field_with_cspec_and_conditions(search_parser):
    spec = search_parser.parse('008[0]/0-7{LDR/5!=\\d}')
    assert spec.type == MarcSpec.FIELD
    assert isinstance(spec.value, FieldSpec)
    assert spec.value.tag == '008'
    assert spec.value.index.start == 0
    assert spec.value.index.end is None
    assert spec.value.cspec.start == 0
    assert spec.value.cspec.end == 7
    assert isinstance(spec.conditions, ConditionExpr)
    assert len(spec.conditions.all) == 1
    assert len(spec.conditions.all[0].any) == 1
    term = spec.conditions.all[0].any[0]
    assert isinstance(term, ConditionTerm)


def test_indicator_with_conditions(search_parser):
    spec = search_parser.parse('650^2{$a~\\Interstitial}')
    assert spec.type == MarcSpec.INDICATOR
    assert isinstance(spec.value, IndicatorSpec)
    assert spec.value.tag == '650'
    assert spec.value.index is None
    assert isinstance(spec.conditions, ConditionExpr)
    assert len(spec.conditions.all) == 1
    assert len(spec.conditions.all[0].any) == 1
    term = spec.conditions.all[0].any[0]
    assert isinstance(term, ConditionTerm)
