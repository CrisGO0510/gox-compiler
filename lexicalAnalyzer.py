import re
import sys

tokens = []
current_token = 0

def tokenize(code):
    global tokens
    token_specification = [
        ('KEYWORD', r'\b(const|var|print|return|break|continue|if|else|while|func|import|true|false)\b'),

        ('ID', r'[A-Za-z_][A-Za-z0-9_]*'),

        ('INTEGER', r'[+-]?[0-9]+'),
        ('FLOAT', r'[+-]?[0-9]*\.[0-9]+'),
        ('CHAR', r"'(\\n|\\x[a-fA-F0-9]{2}|\\'|[^\\'])'"),
        ('BOOL', r"true|false"),

        ('OP', r'(==|!=|<=|>=|&&|\|\||[+\-*/^<>])'),

        ('ASSIGN', r'='),           
        ('SEMI', r';'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('LBRACE', r'\{'),
        ('RBRACE', r'\}'),
        ('COMMA', r','),
        ('DEREF', r'`'),

        ('WHITESPACE', r'\s+'),
        ('MISMATCH', r'.'),
    ]
    
    token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)
    tokens = [(match.lastgroup, match.group()) for match in re.finditer(token_regex, code) if match.lastgroup != 'WHITESPACE']

# # Prueba
# test_code = "var 1a = 10;"
# tokenize(test_code)
# print("TOKEN:", tokens)

if len(sys.argv) != 2:
    print("Usage: python lexicalAnalyzer.py <file_path>")
    sys.exit(1)

file_path = sys.argv[1]

with open(file_path, 'r') as file:
    code = file.read()

tokenize(code)
print("TOKEN:", tokens)
# print("Pertenece a la gramática:" if program() else "No pertenece a la gramática")
