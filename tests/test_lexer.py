# test/test_lexer.py

import pytest
from interpreter.lexer.tokenizer import tokenize, Token, TokenCategory

@pytest.mark.parametrize("source_code, expected_tokens", [
    ("print", [Token(category=TokenCategory.KEYWORD, lexeme="print")]),
    ("variable_name", [
        Token(category=TokenCategory.IDENTIFIER, lexeme="variable_name")
    ]),
    ("+ - =", [
        Token(category=TokenCategory.OPERATOR, lexeme="+"),
        Token(category=TokenCategory.OPERATOR, lexeme="-"),
        Token(category=TokenCategory.OPERATOR, lexeme="=")
    ]),
        ("( )", [
        Token(category=TokenCategory.OPEN_PAREN, lexeme="("),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=")")
    ]),
    ("\n", [Token(category=TokenCategory.NEWLINE, lexeme="\n")]),
    ("   \t", []),
    ("f(x, y)", [
        Token(category=TokenCategory.IDENTIFIER, lexeme="f"),
        Token(category=TokenCategory.OPEN_PAREN, lexeme="("),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.COMMA, lexeme=","),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y"),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=")"),
    ]),
    ("print(x)", [
        Token(category=TokenCategory.KEYWORD, lexeme="print"),
        Token(category=TokenCategory.OPEN_PAREN, lexeme="("),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=")"),
    ]),
    ("x = 10\n", [
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.NUMBER, lexeme=10),
        Token(category=TokenCategory.NEWLINE, lexeme="\n")
    ]),
    ("x = y\n", [
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n")
    ]),
    ("z = x + y\n", [
        Token(category=TokenCategory.IDENTIFIER, lexeme="z"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="+"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n")
    ]),
    ("\n\nz = x + y", [
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="z"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="+"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y")
    ]),
    ("\n\nz = x + y\n\n", [
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="z"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="+"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n")
    ]),
    ("\nx = 10\nz = x + y\n\n", [
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.NUMBER, lexeme=10),
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="z"),
        Token(category=TokenCategory.OPERATOR, lexeme="="),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.OPERATOR, lexeme="+"),
        Token(category=TokenCategory.IDENTIFIER, lexeme="y"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n"),
        Token(category=TokenCategory.NEWLINE, lexeme="\n")
    ]),
    ('x = "hello"', [
        Token(category=TokenCategory.IDENTIFIER, lexeme='x'),
        Token(category=TokenCategory.OPERATOR, lexeme='='),
        Token(category=TokenCategory.STRING, lexeme='"hello"'),
    ]),
    ("x = 'hello'", [
        Token(category=TokenCategory.IDENTIFIER, lexeme='x'),
        Token(category=TokenCategory.OPERATOR, lexeme='='),
        Token(category=TokenCategory.STRING, lexeme="'hello'"),
    ]),
    ("input()",[
        Token(category=TokenCategory.KEYWORD, lexeme="input"),
        Token(category=TokenCategory.OPEN_PAREN, lexeme='('),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=')')
    ]),
    ("max()",[
        Token(category=TokenCategory.KEYWORD, lexeme="max"),
        Token(category=TokenCategory.OPEN_PAREN, lexeme='('),
        Token(category=TokenCategory.CLOSE_PAREN, lexeme=')')
    ])
])
def test_tokenize_cases(
    source_code: str, expected_tokens: list[Token]
) -> None:
    assert tokenize(source_code) == expected_tokens

@pytest.mark.parametrize("source_code, expected_exception, message", [
    (
        "x@2",
        SyntaxError,
        "Error: Could not find a token category for the lexeme: @"
    ),
    (
        """ "hello' """,
        SyntaxError,
        'Error: Could not find a token category for the lexeme: "'
    )
])
def test_tokenize_exceptions(
        source_code: str, expected_exception: Exception, message: str
) -> None:
    with pytest.raises(expected_exception, match=message):
        tokenize(source_code)