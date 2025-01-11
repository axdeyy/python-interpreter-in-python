# intepreter/tokenizer.py

import re
from enum import Enum, auto
from dataclasses import dataclass

class TokenCategory(Enum):
    IDENTIFIER = auto()  # Identifiers (e.g. variable names)
    KEYWORD = auto()     # Reserved keywords (e.g `print`)
    NUMBER = auto()      # Numeric literals (e.g 10)
    OPERATOR = auto()    # Operators (e.g '=', '+')
    PAREN = auto()       # Parentheses (e.g '(', ')')
    COMMA = auto()       # Commas (e.g argument delimiters)
    NEWLINE = auto()     # Line endings
    SKIP = auto()        # Whitespace
    MISMATCH = auto()    # Invalid token

@dataclass
class Token:
    category: TokenCategory
    lexeme: int | str

@dataclass
class TokenSpecification:
    category: TokenCategory
    regex_pattern: str

TOKEN_SPECIFICATIONS: list[TokenSpecification] = [
    TokenSpecification(TokenCategory.KEYWORD, r'\bprint\b'),  # TODO: add more keywords
    TokenSpecification(TokenCategory.IDENTIFIER, r'[A-Za-z_]\w*'),
    TokenSpecification(TokenCategory.NUMBER, r'\d+'),    
    TokenSpecification(TokenCategory.OPERATOR, r'[+=-]'),
    TokenSpecification(TokenCategory.PAREN, r'[()]'),
    TokenSpecification(TokenCategory.NEWLINE, r'\n'),
    TokenSpecification(TokenCategory.SKIP, r'\s+'),
    TokenSpecification(TokenCategory.MISMATCH, r'.'),
]

def tokenize(source_code: str) -> list[Token]:
    token_regex_pattern = '|'.join(f"(?P<{spec.category.name}>{spec.regex_pattern})" for spec in TOKEN_SPECIFICATIONS)
    tokens = []

    for capture in re.finditer(token_regex_pattern, source_code):
        capture_group, capture_value = capture.lastgroup, capture.group()
        token_category = TokenCategory[capture_group]

        # Handle mismatched token 
        if token_category == TokenCategory.MISMATCH:
            raise SyntaxError(f"Error: Could not find a token category for the given lexeme: {capture_value}")
        
        # Handle skip token
        if token_category == TokenCategory.SKIP:
            continue

        # Handle numeric token
        if token_category == TokenCategory.NUMBER:
            capture_value = int(capture_value)
        
        tokens.append(Token(category=token_category, lexeme=capture_value))

    return tokens