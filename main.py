# main.py

from interpreter.lexer.tokenizer import *
from interpreter.parser import *

def test_tokenizer():
    source_code = """
    x = "hello"
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
    print(tokens)
    print(test_parser(tokens))

'''
[
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='='),
 Token(category=<TokenCategory.STRING: 3>, lexeme='"hello"'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='y'),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='='),
 Token(category=<TokenCategory.NUMBER: 4>, lexeme=10),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='f'),
 Token(category=<TokenCategory.OPEN_PAREN: 6>, lexeme='('),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'),
 Token(category=<TokenCategory.COMMA: 8>, lexeme=','),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='y'),
 Token(category=<TokenCategory.CLOSE_PAREN: 7>, lexeme=')'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='z'),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='='),
 Token(category=<TokenCategory.NUMBER: 4>, lexeme=2),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
 Token(category=<TokenCategory.NUMBER: 4>, lexeme=3),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'),
 Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='y'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.KEYWORD: 2>, lexeme='print'),
 Token(category=<TokenCategory.OPEN_PAREN: 6>, lexeme='('),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'),
 Token(category=<TokenCategory.CLOSE_PAREN: 7>, lexeme=')'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n'),
 Token(category=<TokenCategory.KEYWORD: 2>, lexeme='print'),
 Token(category=<TokenCategory.OPEN_PAREN: 6>, lexeme='('),
 Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='z'),
 Token(category=<TokenCategory.CLOSE_PAREN: 7>, lexeme=')'),
 Token(category=<TokenCategory.NEWLINE: 9>, lexeme='\n')
 ]
'''

'''
Program(statements=[
 Assignment(identifier='x', expression=Literal(value='"hello"')),
 Assignment(identifier='y', expression=Literal(value=10)),
 FunctionCall(
    name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='f'),
    arguments=[
        Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x')),
        Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='y'))
    ]
 ),
 Assignment(
    identifier='z',
    expression=BinaryExpression(
        left=Literal(value=2),
        operator=Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
        right=BinaryExpression(
                left=Literal(value=3),
                operator=Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
                right=BinaryExpression(
                    left=Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x')),
                    operator=Token(category=<TokenCategory.OPERATOR: 5>, lexeme='+'),
                    right=Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='y'))
            )
        )
    )
 ),
 FunctionCall(
    name=Token(category=<TokenCategory.KEYWORD: 2>, lexeme='print'),
    arguments=[Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='x'))]
 ),
 FunctionCall(
    name=Token(category=<TokenCategory.KEYWORD: 2>, lexeme='print'),
    arguments=[Variable(name=Token(category=<TokenCategory.IDENTIFIER: 1>, lexeme='z'))]
 )
]) 
'''