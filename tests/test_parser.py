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
    (
        [Token(lexeme="max", category=TokenCategory.KEYWORD),
         Token(lexeme="(", category=TokenCategory.OPEN_PAREN),
         Token(lexeme=")", category=TokenCategory.CLOSE_PAREN)],
        "max", []
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
    "tokens, expected_ast", [
        # Test 1: Basic addition
        (
            [Token(lexeme="x", category=TokenCategory.IDENTIFIER),
             Token(lexeme="+", category=TokenCategory.OPERATOR),
             Token(lexeme="2", category=TokenCategory.NUMBER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="x", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="+", category=TokenCategory.OPERATOR),
                right=Literal(value=2)
            )
        ),
        # Test 2: Basic subtraction
        (
            [Token(lexeme="a", category=TokenCategory.IDENTIFIER),
             Token(lexeme="-", category=TokenCategory.OPERATOR),
             Token(lexeme="3", category=TokenCategory.NUMBER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="a", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="-", category=TokenCategory.OPERATOR),
                right=Literal(value=3)
            )
        ),
        # Test 3: Multiplication
        (
            [Token(lexeme="y", category=TokenCategory.IDENTIFIER),
             Token(lexeme="*", category=TokenCategory.OPERATOR),
             Token(lexeme="4", category=TokenCategory.NUMBER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="y", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="*", category=TokenCategory.OPERATOR),
                right=Literal(value=4)
            )
        ),
        # Test 4: Division
        (
            [Token(lexeme="z", category=TokenCategory.IDENTIFIER),
             Token(lexeme="/", category=TokenCategory.OPERATOR),
             Token(lexeme="5", category=TokenCategory.NUMBER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="z", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="/", category=TokenCategory.OPERATOR),
                right=Literal(value=5)
            )
        ),
        # Test 5: Exponentiation
        (
            [Token(lexeme="b", category=TokenCategory.IDENTIFIER),
             Token(lexeme="^", category=TokenCategory.OPERATOR),
             Token(lexeme="2", category=TokenCategory.NUMBER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="b", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="^", category=TokenCategory.OPERATOR),
                right=Literal(value=2)
            )
        ),
        # Test 6: Nested binary expressions (equal precedence operator)
        (
            [Token(lexeme="a", category=TokenCategory.IDENTIFIER),
             Token(lexeme="+", category=TokenCategory.OPERATOR),
             Token(lexeme="b", category=TokenCategory.IDENTIFIER),
             Token(lexeme="*", category=TokenCategory.OPERATOR),
             Token(lexeme="c", category=TokenCategory.IDENTIFIER)],
            BinaryExpression(
                left=Variable(name=Token(lexeme="a", category=TokenCategory.IDENTIFIER)),
                operator=Token(lexeme="+", category=TokenCategory.OPERATOR),
                right=BinaryExpression(
                    left=Variable(name=Token(lexeme="b", category=TokenCategory.IDENTIFIER)),
                    operator=Token(lexeme="*", category=TokenCategory.OPERATOR),
                    right=Variable(name=Token(lexeme="c", category=TokenCategory.IDENTIFIER))
                )
            )
        ),
        # Test 7: Nested binary expressions (higher precedence operators)
        (
            [Token(lexeme="a", category=TokenCategory.IDENTIFIER),
             Token(lexeme="*", category=TokenCategory.OPERATOR),
             Token(lexeme="b", category=TokenCategory.IDENTIFIER),
             Token(lexeme="+", category=TokenCategory.OPERATOR),
             Token(lexeme="c", category=TokenCategory.IDENTIFIER)],
            BinaryExpression(
                left=BinaryExpression(
                    left=Variable(name=Token(lexeme="a", category=TokenCategory.IDENTIFIER)),
                    operator=Token(lexeme="*", category=TokenCategory.OPERATOR),
                    right=Variable(name=Token(lexeme="b", category=TokenCategory.IDENTIFIER))
                ),
                operator=Token(lexeme="+", category=TokenCategory.OPERATOR),
                right=Variable(name=Token(lexeme="c", category=TokenCategory.IDENTIFIER))
            )
        )
    ]
)
def test_parse_binary_expression(tokens: list[Token], expected_ast: BinaryExpression) -> None:
    parser = Parser(tokens)
    program = parser.parse()
    statement = program.statements[0]

    assert statement == expected_ast


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
