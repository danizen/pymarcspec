from marcspec.model import (
    MarcSpec,
    FieldSpec,
    ConditionExpr,
)


def test_simple_field(search_parser):
    marcspec = search_parser.parse('880')
    assert marcspec.type == MarcSpec.FIELD
    assert isinstance(marcspec.value, FieldSpec)
    assert marcspec.value.tag == '880'
    assert marcspec.value.index is None
    assert marcspec.value.cspec is None
    assert marcspec.conditions is None


def test_field_with_cspec_and_conditions(search_parser):
    marcspec = search_parser.parse('008[0]/0-7{LDR/5!=\\d}')
    assert marcspec.type == MarcSpec.FIELD
    assert isinstance(marcspec.value, FieldSpec)
    assert marcspec.value.tag == '008'
    assert marcspec.value.index.start == 0
    assert marcspec.value.index.end is None
    assert marcspec.value.cspec.start == 0
    assert marcspec.value.cspec.end == 7
    assert isinstance(marcspec.conditions, ConditionExpr)
    assert len(marcspec.conditions.all) == 1
