# intepreter/tokenizer.py

from enum import Enum, auto
from dataclasses import dataclass

class TokenCategory(Enum):
    IDENTIFIER = auto()  # Identifiers (e.g. variable names)
    KEYWORD = auto()     # Reserved keywords (e.g `print`)
    NUMBER = auto()      # Numeric literals (e.g 10)
    OPERATOR = auto()    # Operators (e.g '=', '+')
    PAREN = auto()       # Parentheses (e.g '(', ')')
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
    TokenSpecification(TokenCategory.IDENTIFIER, r'[A-Za-z_]\w*'),
    TokenSpecification(TokenCategory.KEYWORD, r'\bprint\b'),  # TODO: add more keywords
    TokenSpecification(TokenCategory.NUMBER, r'\d+'),    
    TokenSpecification(TokenCategory.OPERATOR, r'[+=-]'),
    TokenSpecification(TokenCategory.PAREN, r'[()]'),
    TokenSpecification(TokenCategory.NEWLINE, r'\n'),
    TokenSpecification(TokenCategory.SKIP, r'\s+'),
    TokenSpecification(TokenCategory.MISMATCH, r'.'),
]

def tokenize(source_code: str) -> list[Token]:
    pass