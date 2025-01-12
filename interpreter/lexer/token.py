# interpeter/lexer/token.py

from dataclasses import dataclass
from .token_categories import TokenCategory

@dataclass(frozen=True)
class Token:
    category: TokenCategory
    lexeme: int | str