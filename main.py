# main.py

from interpreter.lexer import *
from interpreter.parser import *

def test_tokenizer():
    source_code = """
    x = 0
    y = 10

    f(x, y)
    
    z = 2 + 3 + x + y
    print(x)

    print(z)
    
    """

    tokens = tokenize(source_code)
    
    return tokens

def test_parser(tokens: list[Token]):
    p = Parser(tokens)
    return p.parse()

if __name__ == "__main__":
    tokens = test_tokenizer()
    print(test_parser(tokens))


# Program(statements=[Assignment(identifier='x', expression=BinaryExpression(left=Literal(value=2), operator=Token(category=<TokenCategory.OPERATOR: 4>, lexeme='+'), right=BinaryExpression(left=Literal(value=3), operator=Token(category=<TokenCategory.OPERATOR: 4>, lexeme='+'), right=Literal(value=2)))), FunctionCall(name=Token(category=<TokenCategory.KEYWORD: 2>, lexeme='print'), arguments=[Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'))]), FunctionCall(name=Token(category=<TokenCategory.KEYWORD: 
# 2>, lexeme='print'), arguments=[Literal(value=2)])])