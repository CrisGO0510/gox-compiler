from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser
from serialize import to_json

text = """
if a == b {
    a = b;
} else {
    b = a + 2;
}
"""

tokens = list(tokenize(text))
indexToken = 0

print(tokens)

AST = RecursiveDescentParser(tokens, indexToken).program()

print(AST)

print(to_json(AST))
