
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
    subfields = attr.ib()


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
class AbrIndicatorSpec:
    indicator = attr.ib()
    index = attr.ib(default=None)


@attr.s(frozen=True)
class StringCompare:
    value = attr.ib()


@attr.s(frozen=True)
class ConditionTerm:
    op = attr.ib()
    right = attr.ib()
    left = attr.ib(default=None)


@attr.s(frozen=True)
class ConditionExpr:
    any = attr.ib(default=None)
    all = attr.ib(default=None)


@attr.s(frozen=True)
class DataSpec:
    tag = attr.ib()
    subfields = attr.ib()
    subspec = attr.ib()


@attr.s(frozen=True)
class MarcSpec:
    FIELD = 1
    INDICATOR = 2
    VARDATA = 3

    type = attr.ib(type=int)
    value = attr.ib()
    conditions = attr.ib(default=None)
