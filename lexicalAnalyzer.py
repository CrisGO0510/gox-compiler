import re

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

# def match(expected_type):
#     global current_token
#     if current_token < len(tokens) and tokens[current_token][0] == expected_type:
#         current_token += 1
#         return True
#     return False

# def program():
#     while statement():
#         pass
#     return current_token == len(tokens)

# def statement():
#     return assignment() or vardecl() or funcdecl() or if_stmt() or while_stmt() or control_stmt() or print_stmt()

# def assignment():
#     pos = current_token
#     if match('ID') and match('OP') and match('INTEGER') and match('DELIM'):
#         return True
#     current_token = pos
#     return False

# def vardecl():
#     pos = current_token
#     if match('KEYWORD') and match('ID') and match('DELIM'):
#         return True
#     current_token = pos
#     return False

# def print_stmt():
#     pos = current_token
#     if match('KEYWORD') and match('INTEGER') and match('DELIM'):
#         return True
#     current_token = pos
#     return False

# Agregar más funciones para manejar las demás reglas de la gramática.

# Prueba
test_code = "var 1x = 10;"
tokenize(test_code)
print("TOKEN:", tokens)
# print("Pertenece a la gramática:" if program() else "No pertenece a la gramática")
