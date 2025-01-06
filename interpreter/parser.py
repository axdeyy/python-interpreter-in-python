# intepreter/parser.py

from interpreter.ast import Program, Statement, Assignment, Expression
from lexer import Token, TokenCategory
from tkinter.tix import STATUS

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
    
    def parse(self) -> Program:
        statements = []
        while self.current_token_idx < len(self.tokens):
            statements.append(self.parse_statement())
        return Program(statements)

    def _parse_statement(self) -> Statement:
        token = self.tokens[self.current_token_idx]
        match self.peek_next_token().category:
            case TokenCategory.IDENTIFIER:
                if token.lexeme == '=':
                    return self.parse_assignment()
            case _:
                return self.parse_expression()
    
    def _parse_assignment(self) -> Assignment:
        pass

    def _parse_expression(self) -> Expression:
        pass

    def _peek_next_token(self) -> Token:
        return (t := self.tokens[self.current_token_idx + 1]) if t < len(self.tokens) else None