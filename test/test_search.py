from pymarcspec.model import (
    MarcSpec,
    IndicatorFilter,
    FieldFilter,
    SubfieldFilter,
    IndexSpec,
    CharSpec,
)


def test_fieldspec_leader(jama_record):
    spec = MarcSpec(tag='LDR', filter=FieldFilter())
    leader = spec.search(jama_record)
    assert leader == '03244cas a2200721   4500'


def test_fieldspec_subject(jama_record):
    spec = MarcSpec(tag='650', filter=FieldFilter())
    subject = spec.search(jama_record)
    assert subject == 'Medicine https://id.nlm.nih.gov/mesh/D008511'


def test_fieldspec_subjects_dot(jama_record):
    spec = MarcSpec(tag='65.', filter=FieldFilter())
    subjects = spec.search(jama_record, totext=False)
    assert len(subjects) == 2
    assert subjects[0].tag == '650'
    assert subjects[1].tag == '655'


def test_subfield_subjects_a(jama_record):
    spec = MarcSpec(tag='65.', filter=[SubfieldFilter(start='a')])
    subjects = spec.search(jama_record)
    assert subjects == 'Medicine:Periodical'


def test_indicators_two(jama_record):
    spec = MarcSpec(tag='65.', filter=IndicatorFilter(indicator=2))
    indicator2_values = spec.search(jama_record)
    assert indicator2_values == '2:2'


def test_fieldspec_index_first(jama_record):
    spec = MarcSpec(tag='65.', filter=FieldFilter(index=IndexSpec(start=0)))
    subjects = spec.search(jama_record, totext=False)
    assert len(subjects) == 1
    assert subjects[0].tag == '650'


def test_fieldspec_index_last(jama_record):
    spec = MarcSpec(tag='65.', filter=FieldFilter(index=IndexSpec(start='#', end=1)))
    subjects = spec.search(jama_record, totext=False)
    assert len(subjects) == 1
    assert subjects[0].tag == '655'


def test_subfield_index_first(jama_record):
    spec = MarcSpec(tag='65.', filter=[
        SubfieldFilter(start='a', index=IndexSpec(start=0)),
    ])
    subject = spec.search(jama_record)
    assert subject == 'Medicine'


def test_subfield_index_first(jama_record):
    spec = MarcSpec(tag='65.', filter=[
        SubfieldFilter(start='a', index=IndexSpec(start='#', end=1)),
    ])
    subject = spec.search(jama_record)
    assert subject == 'Periodical'


def test_field5_range(jama_record):
    spec = MarcSpec(tag='005', filter=FieldFilter(cspec=CharSpec(start=0, end=8)))
    update_date = spec.search(jama_record)
    assert update_date == '20201127'


def test_leader_range(jama_record):
    spec = MarcSpec(tag='LDR', filter=FieldFilter(cspec=CharSpec(start=9)))
    encoding = spec.search(jama_record)
    assert encoding == 'a'
