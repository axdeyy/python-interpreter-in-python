# interpeter/lexer/token_categories.py

from enum import Enum, auto

class TokenCategory(Enum):
    IDENTIFIER = auto()   # Identifiers (e.g., variable names)
    KEYWORD = auto()      # Reserved keywords (e.g., `print`)
    STRING = auto()       # String literals (e.g "hello world")
    NUMBER = auto()       # Numeric literals (e.g 10)
    OPERATOR = auto()     # Operators (e.g '=', '+')
    OPEN_PAREN = auto()   # Open parenthesis
    CLOSE_PAREN = auto()  # Close parenthesis
    COMMA = auto()        # Commas (e.g argument delimiters)
    NEWLINE = auto()      # Line endings
    SKIP = auto()         # Whitespace
    MISMATCH = auto()     # Invalid token
