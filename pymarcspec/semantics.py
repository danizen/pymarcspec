"""
A tatsu Semantics to simplify the structure of the AST
"""
from tatsu.exceptions import FailedSemantics

from .model import (
    CharSpec,
    IndexSpec,
    SubfieldFilter,
    FieldFilter,
    IndicatorFilter,
    StringCompare,
    ConditionTerm,
    ConditionExpr,
    MarcSpec,
)


class MarcSearchSemantics:
    def position(self, ast):
        return ast if ast == '#' else int(ast)

    def CHARSPEC(self, ast):
        ast = ast[1]
        if ast.range:
            return CharSpec(ast.range.start, ast.range.end)
        else:
            return CharSpec(ast.pos)

    def INDEX(self, ast):
        ast = ast[1]
        if ast.range:
            return IndexSpec(ast.range.start, ast.range.end)
        else:
            return IndexSpec(ast.pos)

    def INDICATOR(self, ast, *args, **kwargs):
        return int(ast)

    def RANGE(self, ast):
        return ast[1]

    def subfieldCode(self, ast):
        return ast.code

    def abrSubfieldSpec(self, ast):
        if ast.range:
            return SubfieldFilter(
                start=ast.range.start,
                end=ast.range.end,
                cspec=ast.cspec,
                index=ast.index
            )
        else:
            return SubfieldFilter(
                start=ast.code,
                cspec=ast.cpsec,
                index=ast.index
            )

    def subfieldSpec(self, ast):
        return MarcSpec(
            tag=ast.tag,
            filter=[ast.codes],
        )

    def abrFieldSpec(self, ast):
        return FieldFilter(
            cspec=ast.cspec,
            index=ast.index
        )

    def fieldSpec(self, ast):
        return MarcSpec(
            tag=ast.tag,
            filter=FieldFilter(
                cspec=ast.cspec,
                index=ast.index
            )
        )

    def indicatorSpec(self, ast):
        return MarcSpec(
            tag=ast.tag,
            filter=IndicatorFilter(
                index=ast.index,
                indicator=ast.ind,
            )
        )

    def abrIndicatorSpec(self, ast):
        return IndicatorFilter(
            indicator=ast.ind,
            index=ast.index
        )

    def comparisonString(self, ast):
        return StringCompare(
            value=ast[1]
        )

    def abbreviation(self, ast):
        if ast.inds:
            return ast.inds
        elif ast.data:
            return ast.data
        elif ast.field:
            return ast.field
        else:
            raise FailedSemantics()

    def subTerm(self, ast):
        if ast.cmp:
            return ast.cmp
        elif ast.inds:
            return ast.inds
        elif ast.data:
            return ast.data
        elif ast.field:
            return ast.field
        elif ast.abr:
            return ast.abr
        else:
            raise FailedSemantics()

    def subTermSet(self, ast):
        return ConditionTerm(
            op=ast.op if ast.op else '?',
            left=ast.left,
            right=ast.right
        )

    def subSpec(self, ast):
        return ConditionExpr(
            any=ast.terms,
        )

    def marcSpec(self, ast):
        condition = ConditionExpr(all=ast.subspec) if ast.subspec else None
        if ast.field:
            return MarcSpec(
                tag=ast.field.tag,
                filter=ast.field.filter,
                condition=condition
            )
        elif ast.inds:
            return MarcSpec(
                tag=ast.inds.tag,
                filter=ast.inds.filter,
                condition=condition
            )
        elif ast.data:
            if ast.data[1] and ast.data[2]:
                # when chaining abrSubfieldSpec, the subSpecs go at the end
                raise FailedSemantics()
            if not ast.data[2]:
                condition = ConditionExpr(all=ast.data[1]) if ast.data[1] else None
                return MarcSpec(
                    tag=ast.data[0].tag,
                    filter=ast.data[0].filter,
                    condition=condition
                )
            else:
                # Build conditional expression form the last chain of subspecs, which is the only that can exist
                last_chain = ast.data[2][-1][1]
                condition = ConditionExpr(all=last_chain) if last_chain else None

                # we need to insist that only of the last possible chain of subspecs exists
                prev_chains = [dat[1] for dat in ast.data[2][:-1]]
                if any(prev_chains):
                    raise FailedSemantics()

                # extent
                dat2_filters = [dat[0] for dat in ast.data[2]]
                return MarcSpec(
                    tag=ast.data[0].tag,
                    filter=ast.data[0].filter + dat2_filters,
                    condition=condition
                )
        else:
            # must be one of fields, indicators, or variable data
            raise FailedSemantics()
