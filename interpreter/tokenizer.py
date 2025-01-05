# intepreter/tokenizer.py

from enum import Enum, auto

class TokenCategory(Enum):
    IDENTIFIER = auto()  # Identifiers (e.g. variable names)
    KEYWORD = auto()     # Reserved keywords (e.g `print`)
    NUMBER = auto()      # Numeric literals (e.g 10)
    OPERATOR = auto()    # Operators (e.g '=', '+')
    PAREN = auto()       # Parentheses (e.g '(', ')')
    NEWLINE = auto()     # Line endings

@dataclass
class Token:
    category: TokenCategory
    value: int | str
