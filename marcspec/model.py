
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
class SubFieldFilter:
    start = attr.ib()
    end = attr.ib(default=None)
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class FieldFilter:
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)


@attr.s(frozen=True)
class IndicatorFilter:
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
class MarcSpec:
    tag = attr.ib()
    filter = attr.ib()
    condition = attr.ib(default=None)
