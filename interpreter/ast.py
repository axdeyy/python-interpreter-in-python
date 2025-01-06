# ast.py

'''
Python Subset Grammar (BNF):

program            ::= statement+
statement          ::= assignment | expression
assignment         ::= identifier '=' expression
expression         ::= function_call | binary_expression | literal
function_call      ::= identifier '(' arguments ')'
arguments          ::= (expression (',' expression)*)?
binary_expression  ::= expression operator expression
identifier         ::= TokenCategory.IDENTIFIER
operator           ::= TokenCategory.OPERATOR
literal            ::= TokenCategory.NUMBER

'''

from abc import ABC
from dataclasses import dataclass
from sre_parse import State
from lexer import TokenCategory

@dataclass
class Statement(ABC):
    pass

@dataclass
class Program:
    statements: list[Statement]

@dataclass
class Expression(Statement):
    pass

@dataclass
class Assignment(Statement):
    identifier: TokenCategory.IDENTIFIER
    expression: Expression

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: TokenCategory.OPERATOR
    right: Expression

@dataclass
class FunctionCall(Expression):
    function_name: TokenCategory.IDENTIFIER | TokenCategory.KEYWORD
    arguments: list[Expression]

@dataclass
class Literal(Expression):
    value: int | str