"""
A tatsu Semantics to simplify the structure of the AST
"""


class MarcSpecSemantics(object):
    def position(self, ast):
        return ast if ast == '#' else int(ast)

    def CHARSPEC(self, ast):
        return ast[1]

    def INDEX(self, ast):
        return ast[1]

    def RANGE(self, ast):
        return ast[1]

    def subfieldCode(self, ast):
        return ast.code

    def marcSpec(self, ast):
        if ast.data and len(ast.data) != 3:
            raise RuntimeError('I thought this could not happen')
        return ast

    def _default(self, ast):
        return ast
