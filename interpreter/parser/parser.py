# intepreter/parser.py

from interpreter.parser.ast import (
    BinaryExpression, FunctionCall, Program, Statement,
    Assignment, Expression, Literal, Variable
)
from ..lexer.tokenizer import Token, TokenCategory

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token_idx = 0
    
    def parse(self) -> Program:
        statements = []

        # Consume leading empty new lines
        self._skip_newlines()

        while self.current_token_idx < len(self.tokens):
            statements.append(self._parse_statement())
            self._skip_newlines()  # Consume empty lines between statements

        return Program(statements)

    def _parse_statement(self) -> Statement:
        if (
            self._current_token().category == TokenCategory.IDENTIFIER 
            and self._peek_next_token().lexeme == '='
        ):
            return self._parse_assignment()
        return self._parse_expression()
    
    def _parse_assignment(self) -> Assignment:
        ''' Assignment: IDENTIFIER '=' expression '''
        identifier_token = self._consume(TokenCategory.IDENTIFIER)
        operator_token = self._consume(TokenCategory.OPERATOR)

        # Error handling for incorrect operator token lexeme
        if operator_token.lexeme != '=':
            raise SyntaxError(
                "Could not parse assignment. Expected '=' operator but got"
                f"{operator_token}"
                )

        expression = self._parse_expression()
        return Assignment(identifier_token.lexeme, expression)

    def _parse_expression(self) -> Expression:
        ''' Expression: FunctionCall | BinaryExpr | Variable | Literal '''
        left = Expression()
        match self._current_token().category:
            case TokenCategory.KEYWORD:
                left = self._parse_function_call(True)
            case TokenCategory.IDENTIFIER:
                if (
                    self._peek_next_token()
                    and self._peek_next_token().category
                    == TokenCategory.OPEN_PAREN
                ):
                    left = self._parse_function_call(False)
                else:
                    left = self._parse_variable()
            case TokenCategory.NUMBER:
                left = self._parse_literal()
        
        # Check for binary expression
        if (
            self._current_token() and 
            self._current_token().category == TokenCategory.OPERATOR
        ):
            return self._parse_binary_expression(left)
        
        return left
    
    def _parse_binary_expression(self, left: Expression) -> BinaryExpression:
        operator = self._consume(TokenCategory.OPERATOR)
        right = self._parse_expression()
        return BinaryExpression(left, operator, right)

    def _parse_function_call(self, keyword: bool) -> FunctionCall:
        function_name = self._consume(
            TokenCategory.KEYWORD if keyword else TokenCategory.IDENTIFIER
        )
        self._consume(TokenCategory.OPEN_PAREN)
        arguments = self._parse_arguments()
        self._consume(TokenCategory.CLOSE_PAREN)
        return FunctionCall(function_name, arguments)

    def _parse_arguments(self) -> list[Expression]:
        # Parse list of arguments
        arguments = []
        while self._current_token().category != TokenCategory.CLOSE_PAREN:
            arguments.append(self._parse_expression())
            if self._current_token().category == TokenCategory.COMMA:
                self._consume(TokenCategory.COMMA)
        return arguments

    def _parse_variable(self) -> Variable:
        token = self._consume(TokenCategory.IDENTIFIER)
        return Variable(token)

    def _parse_literal(self) -> Literal:
        token = self._consume(TokenCategory.NUMBER)
        return Literal(int(token.lexeme))

    def _current_token(self) -> Token:
        return (
            self.tokens[self.current_token_idx]
            if self.current_token_idx < len(self.tokens)
            else None
        )
    
    def _peek_next_token(self) -> Token:
        return (
            self.tokens[self.current_token_idx + 1]
            if self.current_token_idx + 1 < len(self.tokens)
            else None
        )
    
    def _consume(
            self, expected_token_category: TokenCategory
    ) -> Token | None:
        token = self.tokens[self.current_token_idx]
        if token.category != expected_token_category:
            raise SyntaxError(
                f"Expected {expected_token_category}"
                f", but got {token.category}"
            )
        self.current_token_idx += 1
        return token
    
    def _skip_newlines(self):
        while (
            self._current_token() and 
            self._current_token().category == TokenCategory.NEWLINE
        ):
            self._consume(TokenCategory.NEWLINE)