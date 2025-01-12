# interpreter/lexer/__init__.py

"""
Lexer package for tokenizing source code.

This package is responsible for breaking down source code into tokens that can be used
by the parser and other components of the interpreter.

Modules:
    - lexer.py: Main lexer logic for tokenizing input source code.
    - token_categories.py: Defines various token categories (e.g., keywords, numbers).
    - token_specifications.py: Defines the regex patterns used to identify tokens.
    - models.py: Contains dataclasses for representing Tokens and Token Specifications.

Usage:
    To use the lexer, import the 'tokenize' function from the 'lexer.py' module:
    
    from interpreter.lexer.lexer import tokenize
    
    tokens = tokenize(source_code)
    
    This will return a list of tokens based on the provided source code.
"""
