# interpeter/lexer/token_specifications.py

import re
from dataclasses import dataclass
from .token_categories import TokenCategory

@dataclass(frozen=True)
class TokenSpecification:
    category: TokenCategory
    regex_pattern: str

KEYWORDS = {
    "print",
    "sum"
}

# Build KEYWORD regex pattern
keyword_pattern = r'\b(?:' + '|'.join(map(re.escape, KEYWORDS)) + r')\b'

# Token specifications
TOKEN_SPECIFICATIONS = [
    TokenSpecification(TokenCategory.KEYWORD, keyword_pattern),  # Dynamic keyword pattern
    TokenSpecification(TokenCategory.IDENTIFIER, r'[A-Za-z_]\w*'),
    TokenSpecification(TokenCategory.NUMBER, r'\d+'),
    TokenSpecification(TokenCategory.OPERATOR, r'[+=-]'),
    TokenSpecification(TokenCategory.OPEN_PAREN, r'\('),
    TokenSpecification(TokenCategory.CLOSE_PAREN, r'\)'),
    TokenSpecification(TokenCategory.NEWLINE, r'\n'),
    TokenSpecification(TokenCategory.SKIP, r'\s+'),
    TokenSpecification(TokenCategory.COMMA, r','),
    TokenSpecification(TokenCategory.MISMATCH, r'.'),
]