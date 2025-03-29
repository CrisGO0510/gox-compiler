from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser
from serialize import to_json

tokens = list(tokenize("x = 2 || 2"))
indexToken = 0

print(tokens)

AST = RecursiveDescentParser(tokens, indexToken).program()

print(AST)

print(to_json(AST))
