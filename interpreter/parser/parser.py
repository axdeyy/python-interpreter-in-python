# intepreter/parser/parser.py

from interpreter.parser.ast import (
    BinaryExpression, FunctionCall, Program, Statement,
    Assignment, Expression, Literal, Variable
)
from ..lexer.tokenizer import Token, TokenCategory

# Define operator precedence levels
OPERATOR_PRECEDENCE = {
    '+': 1,
    '-': 1,
    '*': 2,
    '/': 2,
    '%': 2,
    '^': 3,  # Exponentiation
    '&&': 0, # Logical AND (lower precedence)
    '||': 0, # Logical OR
}

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
        return self._parse_binary_expression()

    def _parse_binary_expression(self, min_precedence: int = 0) -> Expression:
        # First parse the left-hand side as a primary expression
        left = self._parse_primary_expression()

        # Keep going as long as we find operators with precedence >= min_precedence
        while (
            self._current_token() and
            self._current_token().category == TokenCategory.OPERATOR and
            self.get_precedence(self._current_token().lexeme) >= min_precedence
        ):
            operator = self._current_token()
            current_precedence = self.get_precedence(operator.lexeme)
            
            # Consume the operator
            self._consume(TokenCategory.OPERATOR)
            
            # Parse the right side with a higher precedence to ensure proper associativity
            right = self._parse_binary_expression(current_precedence + 1)
            
            # Create a new binary expression
            left = BinaryExpression(left=left, operator=operator, right=right)
        
        return left

    def _parse_primary_expression(self) -> Expression:
        '''Parse primary expressions (literals, variables, function calls)'''
        match self._current_token().category:
            case TokenCategory.KEYWORD:
                return self._parse_function_call(True)
            case TokenCategory.IDENTIFIER:
                if (
                    self._peek_next_token() and
                    self._peek_next_token().category == TokenCategory.OPEN_PAREN
                ):
                    return self._parse_function_call(False)
                return self._parse_variable()
            case TokenCategory.STRING:
                return self._parse_string_literal()
            case TokenCategory.NUMBER:
                return self._parse_numeric_literal()
            case _:
                raise SyntaxError(f"Unexpected token {self._current_token()}")
        
    def get_precedence(self, operator: str) -> int:
        return OPERATOR_PRECEDENCE.get(operator, -1)  # Default -1 for unknown operators

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
    
    def _parse_string_literal(self) -> Literal:
        token = self._consume(TokenCategory.STRING)
        return Literal(token.lexeme)

    def _parse_numeric_literal(self) -> Literal:
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