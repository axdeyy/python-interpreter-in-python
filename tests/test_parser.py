# test/test_parser.py

import pytest
from interpreter.parser.ast import (
    Assignment, BinaryExpression, FunctionCall, Literal, Variable
)
from interpreter.lexer.tokenizer import Token, TokenCategory
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
    ),
    (
        [Token(lexeme="y", category=TokenCategory.IDENTIFIER),
         Token(lexeme="=", category=TokenCategory.OPERATOR),
         Token(lexeme='"hello"', category=TokenCategory.STRING)],
        "y", '"hello"'
    )
])
def test_parse_assignment(
    tokens: list[Token],
    expected_identifier: str,
    expected_value: int | str
) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]
    
    assert isinstance(statement, Assignment)
    assert statement.identifier == expected_identifier
    assert isinstance(statement.expression, Literal)
    assert statement.expression.value == expected_value


@pytest.mark.parametrize("tokens, expected_function, expected_arguments", [
    (
        [Token(lexeme="print", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
         Token(lexeme="2", category=TokenCategory.NUMBER),
         Token(lexeme=")", category=TokenCategory.CLOSE_PAREN)],
        "print", [2]
    ),
    (
        [Token(lexeme="sum", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
         Token(lexeme="3", category=TokenCategory.NUMBER),
         Token(lexeme=")", category=TokenCategory.CLOSE_PAREN)],
        "sum", [3]
    ),
    (
        [Token(category=TokenCategory.KEYWORD, lexeme="sum"),
        Token(category=TokenCategory.OPEN_PAREN, lexeme="("),
        Token(category=TokenCategory.NUMBER, lexeme=1),
        Token(category=TokenCategory.COMMA, lexeme=","),
        Token(category=TokenCategory.NUMBER, lexeme=2),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=")")],
        "sum", [1, 2]
    ),
    (
        [Token(lexeme="f", category=TokenCategory.IDENTIFIER),
         Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
         Token(lexeme=")", category=TokenCategory.CLOSE_PAREN)],
        "f", []
    ),
    (
        [Token(lexeme="input", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
         Token(lexeme=")", category=TokenCategory.CLOSE_PAREN)],
        "input", []
    ),

])
def test_parse_function_call(
    tokens: list[Token],
    expected_function: str,
    expected_arguments: list[int]
) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]

    assert isinstance(statement, FunctionCall)
    assert statement.name.lexeme == expected_function
    assert len(statement.arguments) == len(expected_arguments)
    for a in statement.arguments:
        assert isinstance(a, Literal)
    for i, a in enumerate(statement.arguments):
        assert a.value == expected_arguments[i]


@pytest.mark.parametrize(
    "tokens, expected_left, expected_operator, expected_right", [
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
    ]
)
def test_parse_binary_expression(
    tokens: list[Token],
    expected_left: int | str,
    expected_operator: str,
    expected_right: int | str
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

@pytest.mark.parametrize("tokens, num_statements", [
    (
        [
            Token(lexeme="x", category=TokenCategory.IDENTIFIER),
            Token(lexeme="=", category=TokenCategory.OPERATOR),
            Token(lexeme="2", category=TokenCategory.NUMBER),
            Token(lexeme="print", category=TokenCategory.KEYWORD),
            Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
            Token(lexeme="x", category=TokenCategory.IDENTIFIER),
            Token(lexeme=")", category=TokenCategory.CLOSE_PAREN),
        ],
        2  # Two statements: assignment and function call
    ),
    (
        [
            Token(lexeme="y", category=TokenCategory.IDENTIFIER),
            Token(lexeme="=", category=TokenCategory.OPERATOR),
            Token(lexeme="5", category=TokenCategory.NUMBER),
            Token(lexeme="sum", category=TokenCategory.KEYWORD),
            Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
            Token(lexeme="10", category=TokenCategory.NUMBER),
            Token(lexeme=")", category=TokenCategory.CLOSE_PAREN),
        ],
        2  # Two statements: assignment and function call
    )
])
def test_parse_multiple_statements(tokens: str, num_statements: int) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    assert len(program.statements) == num_statements
