# intepreter/parser.py

from interpreter.ast import Program, Statement
from lexer import Token

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
    
    def parse(self) -> Program:
        statements = []
        while self.current_token_idx < len(self.tokens):
            statements.append(self.parse_statement())
        return Program(statements)

    def parse_statement(self) -> Statement:
        pass