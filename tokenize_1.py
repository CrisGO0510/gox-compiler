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
    type: str
    value: str
    lineno: int

    def __repr__(self):
        return f"Token({self.type}, {self.value}, {self.lineno})"

def tokenize(text):
    index = 0  # índice actual
    lineno = 1  # número de línea

    while index < len(text):
        # Salta espacios en blanco y cuenta líneas correctamente
        if text[index].isspace():
            if text[index] == '\n':
                lineno += 1
            index += 1
            continue

        # Comentarios de bloque
        if text[index:index+2] == '/*':
            end = text.find('*/', index+2)
            if end >= 0:
                lineno += text[index:end].count('\n')
                index = end + 2
                continue
            else:
                print(f'{lineno}: Comentario no terminado')
                return

        # Comentarios de una línea
        if text[index:index+2] == '//':
            end = text.find('\n', index+2)
            if end >= 0:
                lineno += 1
                index = end + 1
                continue
            else:
                return  # Fin del archivo dentro de un comentario

        # Doble símbolo (&&, ||, <=, >=, ==, !=)
        if text[index:index+2] in TOW_CHAR:
            yield Token(TOW_CHAR[text[index:index+2]], text[index:index+2], lineno)
            index += 2
            continue

        # Símbolos de un solo carácter
        if text[index] in ONE_CHAR:
            yield Token(ONE_CHAR[text[index]], text[index], lineno)
            index += 1
            continue

        # Identificadores y palabras reservadas
        m = NAME_PAT.match(text, index)
        if m:
            value = m.group(0)
            index += len(value)  # Avanzamos el índice completo
            if value in KEYWORDS:
                yield Token(value.upper(), value, lineno)
            else:
                yield Token('ID', value, lineno)
            continue  # Para evitar avanzar `index` dos veces

        # Números flotantes
        m = FLOAT_PAT.match(text, index)
        if m:
            value = m.group(0)
            yield Token('FLOAT', value, lineno)
            index += len(value)
            continue

        # Números enteros
        m = INT_PAT.match(text, index)
        if m:
            value = m.group(0)
            yield Token('INTEGER', value, lineno)
            index += len(value)
            continue

        # Si llega aquí, hay un error léxico
        print(f'{lineno}: Caracter ilegal {text[index]!r}')
        index += 1  # Evitar bucles infinitos
        continue

def main(argv):
    if len(argv) != 2:
        raise SystemExit(f'Uso: {argv[0]} <archivo>')

    with open(argv[1]) as file:
        text = file.read()

    for token in tokenize(text):
        print(token)

if __name__ == '__main__':
    import sys
    main(sys.argv)
