# test/test_lexer.py

import pytest
from interpreter.lexer import tokenize, Token, TokenCategory

@pytest.mark.parametrize("source_code, expected_tokens", [
    ("print", [Token(category=TokenCategory.KEYWORD, lexeme="print")]),
    ("variable_name", [Token(category=TokenCategory.IDENTIFIER, lexeme="variable_name")]),
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
])
def test_tokenize_cases(source_code, expected_tokens):
    assert tokenize(source_code) == expected_tokens