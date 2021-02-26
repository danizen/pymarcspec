"""
A tatsu Semantics to simplify the structure of the AST
"""
from .model import (
    CharSpec,
    IndexSpec,
    AbrSubfieldSpec,
    SubfieldSpec,
    AbrFieldSpec,
    FieldSpec,
    IndicatorSpec,
)


class MarcSpecSemantics:
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
            start=ast.codes.start,
            end=ast.codes.end,
            cspec=ast.codes.cspec,
            index=ast.codes.index
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

    def marcSpec(self, ast):
        if ast.data and len(ast.data) != 3:
            raise RuntimeError('I thought this could not happen')
        return ast
