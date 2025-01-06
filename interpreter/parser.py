# intepreter/parser.py

from interpreter.ast import FunctionCall, Program, Statement, Assignment, Expression, Literal
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
        if operator_token.lexeme != '=':
            raise SyntaxError(f"Could not parse assignment. Expected '=' operator but got {operator_token}")

        expression = self._parse_expression()
        return Assignment(identifier_token.lexeme, expression)


    def _parse_expression(self) -> Expression:
        ''' Expression: FunctionCall | BinaryExpression | Literal '''
        token = self.tokens[self.current_token_idx]
        match token.category:
            case TokenCategory.IDENTIFIER:
                function_name = self._consume(TokenCategory.IDENTIFIER)
                self._consume(TokenCategory.PAREN)
                arguments = self._parse_arguments()
                self._consume(TokenCategory.PAREN)
                return FunctionCall(function_name, arguments)
            case TokenCategory.NUMBER:
                return self._parse_literal()
            case _:
                return self._parse_binary_expression()
    
    def _parse_arguments(self) -> list[Expression]:
        # Basic single argument parsing
        argument = self._parse_expression()
        return [argument]

    def _parse_literal(self) -> Literal:
        token = self._consume(TokenCategory.NUMBER)
        return Literal(int(token.lexeme))

    def _parse_binary_expression(self) -> Literal:
        pass

    def _peek_next_token(self) -> Token:
        return self.tokens[i := (self.current_token_idx + 1)] if i < len(self.tokens) else None
    
    def _consume(self, expected_token_category: TokenCategory) -> Token | None:
        token = self.tokens[self.current_token_idx]
        if token.category != expected_token_category:
            raise SyntaxError(f"Expected {expected_token_category}, but got {token.category}")
        self.current_token_idx += 1
        return token