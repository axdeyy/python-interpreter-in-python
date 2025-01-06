# ast.py

'''
Parser Grammar (BNF):

program            ::= statement+
statement          ::= assignment | expression
assignment         ::= IDENTIFIER '=' expression
expression         ::= function_call | binary_expression | literal
function_call      ::= IDENTIFIER '(' arguments ')'
arguments          ::= (expression (',' expression)*)?
binary_expression  ::= expression operator expression
operator           ::= '+' | '-' | '*' | '/'
literal            ::= NUMBER

'''

from abc import ABC
from dataclasses import dataclass

@dataclass
class Expression(ABC):
    pass