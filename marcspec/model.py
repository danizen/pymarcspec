
"""
Structure of the data used for a search, produced by semantic parser.
"""
import attr


@attr.s(frozen=True)
class IndexSpec:
    start = attr.ib()
    end = attr.ib(default=None)


@attr.s(frozen=True)
class CharSpec:
    start = attr.ib()
    end = attr.ib(default=None)


@attr.s(frozen=True)
class AbrSubfieldSpec:
    start = attr.ib()
    end = attr.ib(default=None)
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class SubfieldSpec:
    tag = attr.ib()
    start = attr.ib()
    end = attr.ib(default=None)
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class AbrFieldSpec:
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class FieldSpec:
    tag = attr.ib()
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class IndicatorSpec:
    tag = attr.ib()
    indicator = attr.ib()
    index = attr.ib(default=None)


@attr.s(frozen=True)
class ComparisonCondition:
    pass

@attr.s(frozen=True)
class ConditionalSpec:
    terms = attr.ib()


@attr.s(frozen=True)
class DataSpec:
    tag = attr.ib()
    subfields = attr.ib()
    subspec = attr.ib()
