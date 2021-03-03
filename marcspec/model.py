
"""
Structure of the data used for a search, produced by semantic parser.
"""
import attr
import itertools
import re


@attr.s(frozen=True)
class IndexSpec:
    start = attr.ib()
    end = attr.ib(default=None)


@attr.s(frozen=True)
class CharSpec:
    start = attr.ib()
    end = attr.ib(default=None)


@attr.s(frozen=True)
class SubfieldFilter:
    start = attr.ib()
    end = attr.ib(default=None)
    cspec = attr.ib(default=None)
    index = attr.ib(default=None)

    def codes(self):
        if self.end:
            return [chr(i) for i in range(ord('a'), ord('c')+1)]
        else:
            return [self.start]


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
    filter = attr.ib(default=None)
    condition = attr.ib(default=None)

    def get_fields(self, record):
        if self.tag == 'LDR':
            return [record.leader]
        elif '.' not in self.tag:
            return record.get_fields(self.tag)
        else:
            expr = re.compile(self.tag + '$')
            return [field for field in record.get_fields() if expr.match(field.tag)]

    def get_index(self):
        if not self.filter:
            index = None
        elif isinstance(self.filter, list) and len(self.filter) > 0:
            index = self.filter[0].index
        else:
            index = self.filter.index
        return index

    def filter_by_index(self, fields):
        # needs to be safe if the list of fields contains nothing
        index = self.get_index()
        if index is None:
            return fields
        start = -1 if index.start == '#' else index.start
        end = len(fields) if index.end == '#' else index.end
        if end is None:
            return [fields[start]]
        else:
            end = max(end, len(fields))
            if start == -1:
                end += 1
            return fields[start:end]

    def search(self, record, totext=True, field_delimiter=':', subfield_delimiter=','):
        fields = self.get_fields(record)
        results = self.filter_by_index(fields)
        if isinstance(self.filter, FieldFilter) or not self.filter:
            if totext:
                results = [
                    field.value() if hasattr(field, 'value') else field
                    for field in results
                ]
            # apply cspec to field value
        elif isinstance(self.filter, IndicatorFilter):
            results = [
                field.indicator1 if self.filter.indicator == 1 else field.indicator2
                for field in results
            ]
        else:
            # better be subfield filters
            assert isinstance(self.filter, list)
            assert all(isinstance(f, SubfieldFilter) for f in self.filter)
            # get all the codes
            subfield_codes = [
                code
                for f in self.filter
                for code in f.codes()
            ]
            # get the field results for all fields in the results
            results = [f.get_subfields(*subfield_codes) for f in results]
            # apply cspec to subfields
            if totext:
                results = [subfield_delimiter.join(values) for values in results]
        if totext:
            return field_delimiter.join(results)
        return results
