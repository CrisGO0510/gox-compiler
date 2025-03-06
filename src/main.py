from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser

tokens = list(tokenize("return 2 + 3"))
indexToken = 0

print(tokens)

# AST = RecursiveDescentParser(tokens, indexToken).program()

# print(AST)
