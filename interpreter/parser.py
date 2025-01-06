# intepreter/parser.py

from interpreter.ast import Program, Statement, Assignment, Expression
from lexer import Token, TokenCategory

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
        ''' Assignment: IDENTIFIER '=' expression '''
        identifier_token = self._consume(TokenCategory.IDENTIFIER)
        operator_token = self._consume(TokenCategory.OPERATOR)

        # Error handling for incorrect operator token lexeme
        if operator_token.lexeme != '+':
            raise SyntaxError(f"Could not parse Assignment. Expected '=' operator but got {operator_token}")

        expression = self._parse_expression()
        return Assignment(identifier=identifier_token.lexeme, expression=expression)


    def _parse_expression(self) -> Expression:
        pass

    def _peek_next_token(self) -> Token:
        return (t := self.tokens[self.current_token_idx + 1]) if t < len(self.tokens) else None
    
    def _consume(self, expected_token_category: TokenCategory) -> Token | None:
        token = self.tokens[self.current_token_idx]
        if token.category != expected_token_category:
            raise SyntaxError(f"Expected {expected_token_category}, but got {token.category}")
        self.current_token_idx += 1
        return token