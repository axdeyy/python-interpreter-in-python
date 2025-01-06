# main.py

from interpreter.tokenizer import *

def test_tokenizer():
    source_code = """x = 10
    y = 20
    z = x + y
    print(z)"""

    tokens = tokenize(source_code)
    
    for token in tokens:
        print(token)

if __name__ == "__main__":
    test_tokenizer()