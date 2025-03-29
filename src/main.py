from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser
from serialize import to_json

text = """
var c int = 5 + -2;
"""

tokens = list(tokenize(text))
indexToken = 0

print(tokens)

AST = RecursiveDescentParser(tokens, indexToken).program()

print(AST)

print(to_json(AST))
