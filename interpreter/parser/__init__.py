# interpreter/parser/__init__.py

"""
Parser package for interpreting tokenized source code.

This package converts the tokenized input from the lexer into an Abstract Syntax Tree (AST), 
which represents the structure of the source code.

Modules:
    - parser.py: Contains the `Parser` class, which parses tokens into an AST.
    - ast.py: Defines the AST structure, including nodes like `Program`, `Statement`, and `Expression`.

Usage:
    To use the parser, instantiate the `Parser` class with a list of tokens and call its `parse()` method:
    
    from interpreter.lexer import lexer
    from interpreter.parser import parser

    tokens = lexer.tokenize(source_code)
    parser_instance = parser.Parser(tokens)
    program = parser_instance.parse()

    The resulting `program` is an AST that represents the source code.

Error Handling:
    Syntax errors encountered during parsing will raise `SyntaxError` exceptions with helpful messages.

Notes:
    - The parser currently supports a simple subset of Python-like syntax.
    - Future improvements could include enhanced error recovery and support for more complex syntax.

"""
