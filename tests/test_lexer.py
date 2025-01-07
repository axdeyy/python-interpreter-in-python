# test/test_lexer.py

import pytest
from interpreter.lexer import tokenize, Token, TokenCategory

@pytest.mark.parametrize("source_code, expected_tokens", [
    ("print", [Token(category=TokenCategory.KEYWORD, lexeme="print")])
])
def test_tokenize_cases(source_code, expected_tokens):
    assert tokenize(source_code) == expected_tokens