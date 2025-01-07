# test/test_parser.py

from re import A
import pytest
from interpreter.ast import Assignment, Literal
from interpreter.lexer import Token, TokenCategory
from interpreter.parser import Parser

def test_parse_assignment(
    tokens: list[Token],
    expected_identifier: str,
    expected_value: int
) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]
    
    assert isinstance(statement, Assignment)
    assert statement.identifier == expected_identifier
    assert isinstance(statement.expression, Literal)
    assert statement.expression.value == expected_value