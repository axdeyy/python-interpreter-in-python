# test/test_lexer.py

import pytest
from interpreter.lexer import tokenize, Token, TokenCategory

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
        Token(category=TokenCategory.PAREN, lexeme="("),
        Token(category=TokenCategory.PAREN, lexeme=")")
    ]),
    ("\n", [Token(category=TokenCategory.NEWLINE, lexeme="\n")]),
    ("   \t", []),
    ("print(x)", [
        Token(category=TokenCategory.KEYWORD, lexeme="print"),
        Token(category=TokenCategory.PAREN, lexeme="("),
        Token(category=TokenCategory.IDENTIFIER, lexeme="x"),
        Token(category=TokenCategory.PAREN, lexeme=")"),
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
])
def test_tokenize_cases(
    source_code: str, expected_tokens: list[Token]
) -> None:
    assert tokenize(source_code) == expected_tokens

    
def test_tokenize_exceptions(
        source_code: str, expected_exception: Exception, message: str
) -> None:
    with pytest.raises(expected_exception, match=message):
        tokenize(source_code)