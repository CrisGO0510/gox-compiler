from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser

tokens = list(tokenize("const x = 3 + 2"))
indexToken = 0

print(tokens)

AST = RecursiveDescentParser(tokens, indexToken).program()

print(AST)
