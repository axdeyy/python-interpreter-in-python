# interpeter/lexer/tokenizer.py

import re
from .token import Token
from .token_categories import TokenCategory
from .token_specifications import TOKEN_REGEX_PATTERNS

def tokenize(source_code: str) -> list[Token]:
    # Build the combined regex pattern for all token specifications

    tokens = []
    
    # Use regex to find all tokens
    for capture in re.finditer(TOKEN_REGEX_PATTERNS, source_code):
        capture_group, capture_value = capture.lastgroup, capture.group()
        token_category = TokenCategory[capture_group]

        # Handle mismatched token
        if token_category == TokenCategory.MISMATCH:
            raise SyntaxError(
                "Error: Could not find a token category for the lexeme: "
                f"{capture_value}"
            )

        # Handle skip token (whitespace)
        if token_category == TokenCategory.SKIP:
            continue

        # Handle numeric token conversion
        if token_category == TokenCategory.NUMBER:
            capture_value = int(capture_value)
        
        # Add valid token to the list
        tokens.append(Token(category=token_category, lexeme=capture_value))

    return tokens
