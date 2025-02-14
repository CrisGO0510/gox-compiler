# tokenize.py
'''
El papel del Analizador Léxico es convertir texto dentro 
de simbolos reconocidos.

El Analizador de GOX es requerido para reconocer los 
siguientes simbolos. Los nombres sugeridos para el token 
está al lado izquierdo. La coincidencia de texto esta a la
derecha.

Palabras Reservadas:
    CONST       : 'const'
    VAR         : 'var'
    PRINT       : 'print'
    RETURN      : 'return'
    BREAK       : 'break'
    CONTINUE    : 'continue'
    IF          : 'if'
    ELSE        : 'else'
    WHILE       : 'while'
    FUNC        : 'func'
    IMPORT      : 'import'
    TRUE        : 'true'
    FALSE       : 'false'

Identificadores:
    ID          : Texto que comienza con una letra y 
                    seguido de letras y digitos.
                  Ejemplos: 'a', 'abc', 'a1', 'a1b2c3'
                  '_abc', 'a_b_c'

Literales:
    INTEGER     : 123 (decimales)

    FLOAT       : 123.456
                : 123.
                : .456  

    CHAR        : 'a'   (caracter simple - byte)
                : '\n'  (caracter de escape)
                : '\x41' (caracter hexadecimal)
                : '\''  (comilla simple)

Operadores:
    PLUS        : '+'
    MINUS       : '-'
    TIMES       : '*'
    DIVIDE      : '/'
    LT          : '<'
    LE          : '<='
    GT          : '>'
    GE          : '>='
    EQ          : '=='
    NE          : '!='
    LAND        : '&&'
    LOR         : '||'
    GROW        : '^'

Simbolos Miselaneos:
    ASSIGN      : '='           
    SEMI        : ';'
    LPAREN      : '('
    RPAREN      : ')'
    LBRACE      : '{'
    RBRACE      : '}'
    COMMA       : ','
    DEREF       : '`'

Comentarios: Para ser ignorados
    //          : Comentario de una linea
    /* ... */   : Comentario de multiples lineas

Errores: Su analizador lexico debe reconocer opcionalmente
y reportar los siguientes errores:

    lineno: Caracter ilegal 'c'
    lineno: caracter no terminado 'c
    lineno: Comentario no terminado
'''
from dataclasses import dataclass
import re

from rich import print

TOW_CHAR = {
    '&&': 'LAND',
    '||': 'LOR',
    '<=': 'LE',
    '>=': 'GE',
    '==': 'EQ',
    '!=': 'NE',
}

ONE_CHAR = {
    '+': 'PLUS',
    '-': 'MINUS',
    '*': 'TIMES',
    '/': 'DIVIDE',
    '<': 'LT',
    '>': 'GT',
    '^': 'GROW',
    '=': 'ASSIGN',
    ';': 'SEMI',
    '(': 'LPAREN',
    ')': 'RPAREN',
    '{': 'LBRACE',
    '}': 'RBRACE',
    ',': 'COMMA',
    '`': 'DEREF',
}

NAME_PAT = re.compile(r'[a-zA-Z_]\w*')
FLOAT_PAT = re.compile(r'(\d+\.\d*)|(\d*\.\d+)')
INT_PAT = re.compile(r'\d+')

KEYWORDS = {
    'const', 'var', 'print', 'return', 'break', 'continue',
    'if', 'else', 'while', 'func', 'import', 'true', 'false',
}

@dataclass
class Token:
    def __init__(self, type:str, value:str, lineno:int):
        self.type = type
        self.value = value
        self.lineno = lineno
    #type: str
    #value: str
    #lineno: int

def tokenize(text):
    index = 0 #indice actual
    lineno = 1 #numero de linea

    while index < len(text):
        # Salta espacios en blanco
        if text[index].isspace():
            index += 1
            continue
        elif text[index] == '\n': # Salta nueva linea
            lineno += 1
            index += 1
            continue
        elif text[index:index+2] == '/*': # Salta comentario multilinea
            end = text.find('*/', index+2)
            if end >= 0:
                lineo += text[index:end].count('\n')
                index = end + 2
                continue
            else:
                print(f'{lineno}: Comentario no terminado')
                return
        elif text[index:index+2] == '//': # Salta comentario de una linea
            end = text.find('\n', index+2)
            if end >= 0:
                lineno += 1
                index = end + 1
                continue
            else:
                #nuestro programa no debe caer en este caso
                return
        #coincidencia de simbolos por expresiones regulares
        m = NAME_PAT.match(text, index)
        if m:
            value = m.group(0)
            if value in KEYWORDS: 
                yield Token(value.upper(), value, lineno)
            else:
                yield Token('ID', value, lineno)
        index += 1
        #print(text[index], end='')
        #index += 1  

def main(argv):
    if len(argv) != 2:
        raise SystemExit(f'Uso: {argv[0]} <archivo>')

    with open(argv[1]) as file:
        text = file.read()
    
    for token in  tokenize(text):
        print(token)

if __name__ == '__main__':
    import sys
    main(sys.argv)