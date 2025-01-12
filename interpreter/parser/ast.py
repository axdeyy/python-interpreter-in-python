# interpeter/parser/ast.py

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
from ..lexer.tokenizer import Token

@dataclass(frozen=True)
class Statement(ABC):
    pass

@dataclass(frozen=True)
class Program:
    statements: list[Statement]

@dataclass(frozen=True)
class Expression(Statement):
    pass

@dataclass(frozen=True)
class Assignment(Statement):
    identifier: Token
    expression: Expression

@dataclass(frozen=True)
class BinaryExpression(Expression):
    left: Expression
    operator: Token
    right: Expression

@dataclass(frozen=True)
class FunctionCall(Expression):
    name: Token
    arguments: list[Expression]

@dataclass(frozen=True)
class Variable(Expression):
    name: Token

@dataclass(frozen=True)
class Literal(Expression):
    value: int | str