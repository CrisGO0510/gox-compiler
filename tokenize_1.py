# tokenize.py
r'''
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
