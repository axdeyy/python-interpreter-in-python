# ast.py

'''
Python Subset Grammar (BNF):

program            ::= statement+
statement          ::= assignment | expression
assignment         ::= identifier '=' expression
expression         ::= function_call | binary_expression | identifier | literal
function_call      ::= identifier '(' arguments ')'
arguments          ::= (expression (',' expression)*)?
binary_expression  ::= expression operator expression
identifier         ::= TokenCategory.IDENTIFIER
operator           ::= TokenCategory.OPERATOR
literal            ::= TokenCategory.NUMBER

'''

from abc import ABC
from dataclasses import dataclass
from os import name
from .lexer import Token

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
    identifier: Token
    expression: Expression

@dataclass
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression

@dataclass
class FunctionCall(Expression):
    name: Token
    arguments: list[Expression]

@dataclass
class Variable(Expression):
    name: Token

@dataclass
class Literal(Expression):
    value: int | str