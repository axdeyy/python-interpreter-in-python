# test/test_parser.py

from re import A
import pytest
from interpreter.ast import Assignment, BinaryExpression, FunctionCall, Literal, Variable
from interpreter.lexer import Token, TokenCategory
from interpreter.parser import Parser

@pytest.mark.parametrize("tokens, expected_identifier, expected_value", [
    (
        [Token(lexeme="x", category=TokenCategory.IDENTIFIER),
         Token(lexeme="=", category=TokenCategory.OPERATOR),
         Token(lexeme="2", category=TokenCategory.NUMBER)],
        "x", 2
    ),
    (
        [Token(lexeme="y", category=TokenCategory.IDENTIFIER),
         Token(lexeme="=", category=TokenCategory.OPERATOR),
         Token(lexeme="10", category=TokenCategory.NUMBER)],
        "y", 10
    )
])
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


@pytest.mark.parametrize("tokens, expected_function, expected_argument", [
    (
        [Token(lexeme="print", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.PAREN),
         Token(lexeme="2", category=TokenCategory.NUMBER),
         Token(lexeme=")", category=TokenCategory.PAREN)],
        "print", 2
    ),
    (
        [Token(lexeme="sum", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.PAREN),
         Token(lexeme="3", category=TokenCategory.NUMBER),
         Token(lexeme=")", category=TokenCategory.PAREN)],
        "sum", 3
    )
])
def test_parse_function_call(
    tokens: list[Token],
    expected_function: str,
    expected_argument: int
) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]

    assert isinstance(statement, FunctionCall)
    assert statement.name.lexeme == expected_function
    assert len(statement.arguments) == 1
    assert isinstance(statement.arguments[0], Literal)
    assert statement.arguments[0].value == expected_argument


@pytest.mark.parametrize("tokens, expected_left, expected_operator, expected_right", [
    (
        [Token(lexeme="x", category=TokenCategory.IDENTIFIER),
         Token(lexeme="+", category=TokenCategory.OPERATOR),
         Token(lexeme="2", category=TokenCategory.NUMBER)],
        "x", "+", 2
    ),
    (
        [Token(lexeme="a", category=TokenCategory.IDENTIFIER),
         Token(lexeme="-", category=TokenCategory.OPERATOR),
         Token(lexeme="3", category=TokenCategory.NUMBER)],
        "a", "-", 3
    )
])
def test_parse_binary_expression(
    tokens: list[Token],
    expected_left: str,
    expected_operator: str,
    expected_right: int
) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]

    assert isinstance(statement, BinaryExpression)
    assert isinstance(statement.left, Variable)
    assert statement.left.name.lexeme == expected_left
    assert statement.operator.lexeme == expected_operator
    assert isinstance(statement.right, Literal)
    assert statement.right.value == expected_right


def test_parse_multiple_statements(tokens: str, num_statements: int) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == num_statements
