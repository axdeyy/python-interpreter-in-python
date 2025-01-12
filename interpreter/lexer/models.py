from dataclasses import dataclass
from .token_categories import TokenCategory

@dataclass
class Token:
    category: TokenCategory
    lexeme: int | str

@dataclass
class TokenSpecification:
    category: TokenCategory
    regex_pattern: str
