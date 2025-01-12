# main.py

import token
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