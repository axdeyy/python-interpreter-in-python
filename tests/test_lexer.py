# test/test_lexer.py

import pytest
from interpreter.lexer import tokenize, Token, TokenCategory

def test_tokenize_cases(source_code, expected_tokens):
    assert tokenize(source_code) == expected_tokens