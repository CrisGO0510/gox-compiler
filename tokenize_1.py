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
        if text[index].isspace():
            if text[index] == '\n':
                lineno += 1
            index += 1
            continue

        if text[index:index+2] == '/*':
            end = text.find('*/', index+2)
            if end >= 0:
                lineno += text[index:end].count('\n')
                index = end + 2
                continue
            else:
                print("[red]ERROR:[/red]", f"Comentario no terminado", lineno)
                yield Token("ERROR", f"Comentario no terminado", lineno)
                index += 2
                continue

        if text[index:index+2] == '//':
            end = text.find('\n', index+2)
            if end >= 0:
                lineno += 1
                index = end + 1
                continue
            else:
                return  

        if text[index:index+2] in TOW_CHAR:
            yield Token(TOW_CHAR[text[index:index+2]], text[index:index+2], lineno)
            index += 2
            continue

        if text[index] in ONE_CHAR:
            yield Token(ONE_CHAR[text[index]], text[index], lineno)
            index += 1
            continue

        m = NAME_PAT.match(text, index)
        if m:
            value = m.group(0)
            index += len(value)
            if value in KEYWORDS:
                yield Token(value.upper(), value, lineno)
            else:
                yield Token('ID', value, lineno)
            continue

        m = FLOAT_PAT.match(text, index)
        if m:
            value = m.group(0)
            yield Token('FLOAT', value, lineno)
            index += len(value)
            continue

        m = INT_PAT.match(text, index)
        if m:
            value = m.group(0)
            yield Token('INTEGER', value, lineno)
            index += len(value)
            continue

        if text[index] == "'":
            if index + 2 < len(text) and text[index + 2] == "'":
                char_value = text[index + 1]
                yield Token("CHAR", char_value, lineno)
                index += 3
                continue
            elif text[index + 1:index + 3] in ["\\n", "\\t", "\\x"]:
                char_value = text[index + 1:index + 3]
                yield Token("CHAR", char_value, lineno)
                index += 4
                continue
            else:
                
                print("[red]ERROR:[/red]", f"Caracter no válido o no terminado {text[index]!r}", lineno)
                yield Token("ERROR", f"Caracter no válido o no terminado {text[index]!r}", lineno)
                index += 1
                continue

        # Si llega aquí, es un carácter ilegal
        print("[red]ERROR:[/red]", f"Caracter ilegal {text[index]!r}", lineno)
        yield Token("ERROR", f"Caracter ilegal {text[index]!r}", lineno)
        index += 1


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
