"""
A tatsu Semantics to simplify the structure of the AST
"""
from tatsu.exceptions import FailedSemantics

from .model import (
    CharSpec,
    IndexSpec,
    AbrSubfieldSpec,
    SubfieldSpec,
    AbrFieldSpec,
    FieldSpec,
    AbrIndicatorSpec,
    IndicatorSpec,
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
            return AbrSubfieldSpec(
                start=ast.range.start,
                end=ast.range.end,
                cspec=ast.cspec,
                index=ast.index
            )
        else:
            return AbrSubfieldSpec(
                start=ast.code,
                cspec=ast.cpsec,
                index=ast.index
            )

    def subfieldSpec(self, ast):
        return SubfieldSpec(
            tag=ast.tag,
            subfields=[ast.codes],
        )

    def abrFieldSpec(self, ast):
        return AbrFieldSpec(
            cspec=ast.cspec,
            index=ast.index
        )

    def fieldSpec(self, ast):
        return FieldSpec(
            tag=ast.tag,
            cspec=ast.cspec,
            index=ast.index
        )

    def indicatorSpec(self, ast):
        return IndicatorSpec(
            tag=ast.tag,
            indicator=ast.ind,
            index=ast.index
        )

    def abrIndicatorSpec(self, ast):
        return AbrIndicatorSpec(
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
        conditions = ConditionExpr(all=ast.subspec) if ast.subspec else None
        if ast.field:
            return MarcSpec(
                type=MarcSpec.FIELD,
                value=ast.field,
                conditions=conditions
            )
        elif ast.inds:
            return MarcSpec(
                type=MarcSpec.INDICATOR,
                value=ast.inds,
                conditions=conditions
            )
        elif ast.data:
            if ast.data[1] and ast.data[2]:
                # when chaining abrSubfieldSpec, the subSpecs go at the end
                raise FailedSemantics()
            if not ast.data[2]:
                conditions = ConditionExpr(all=ast.data[1]) if ast.data[1] else None
                return MarcSpec(
                    type=MarcSpec.VARDATA,
                    value=ast.data[0],
                    conditions=conditions
                )
            else:
                # need to consolidate data[2] abbreviated subfield specs into a new SubfieldSpec
                # need to build contitions
                return ast
        else:
            # must be one of fields, indicators, or variable data
            raise FailedSemantics()
