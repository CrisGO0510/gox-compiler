import unittest
import sys
import os

# Obtener la ruta absoluta del directorio raíz del proyecto
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from lexer import Token, tokenize


class TestLexer(unittest.TestCase):

    def test_palabras_reservadas(self):
        tokens = list(
            tokenize(
                "const var print return break continue if else while func import true false"
            )
        )
        palabras = [
            "CONST",
            "VAR",
            "PRINT",
            "RETURN",
            "BREAK",
            "CONTINUE",
            "IF",
            "ELSE",
            "WHILE",
            "FUNC",
            "IMPORT",
            "TRUE",
            "FALSE",
        ]
        valores = [
            "const",
            "var",
            "print",
            "return",
            "break",
            "continue",
            "if",
            "else",
            "while",
            "func",
            "import",
            "true",
            "false",
        ]
        for i, token in enumerate(tokens):
            self.assertEqual(token, Token(palabras[i], valores[i], 1))

    def test_identificadores(self):
        tokens = list(tokenize("variable _var1 a1b2c3"))
        self.assertEqual(
            tokens,
            [
                Token("ID", "variable", 1),
                Token("ID", "_var1", 1),
                Token("ID", "a1b2c3", 1),
            ],
        )

    def test_numeros(self):
        tokens = list(tokenize("123 45.67 .456 123."))
        self.assertEqual(
            tokens,
            [
                Token("INTEGER", "123", 1),
                Token("FLOAT", "45.67", 1),
                Token("FLOAT", ".456", 1),
                Token("FLOAT", "123.", 1),
            ],
        )

    def test_operadores(self):
        tokens = list(tokenize("+ - * / <= >= == != && || ^"))
        tipos = [
            "PLUS",
            "MINUS",
            "TIMES",
            "DIVIDE",
            "LE",
            "GE",
            "EQ",
            "NE",
            "LAND",
            "LOR",
            "GROW",
        ]
        valores = ["+", "-", "*", "/", "<=", ">=", "==", "!=", "&&", "||", "^"]
        self.assertEqual(
            tokens, [Token(tipos[i], valores[i], 1) for i in range(len(tipos))]
        )

    def test_simbolos_miscelaneos(self):
        tokens = list(tokenize("= ; ( ) { } , `"))
        tipos = [
            "ASSIGN",
            "SEMI",
            "LPAREN",
            "RPAREN",
            "LBRACE",
            "RBRACE",
            "COMMA",
            "DEREF",
        ]
        valores = ["=", ";", "(", ")", "{", "}", ",", "`"]
        self.assertEqual(
            tokens, [Token(tipos[i], valores[i], 1) for i in range(len(tipos))]
        )

    def test_comentarios(self):
        tokens = list(tokenize("var x = 5; // comentario"))
        self.assertEqual(
            tokens,
            [
                Token("VAR", "var", 1),
                Token("ID", "x", 1),
                Token("ASSIGN", "=", 1),
                Token("INTEGER", "5", 1),
                Token("SEMI", ";", 1),
            ],
        )

    def test_comentario_bloque(self):
        tokens = list(tokenize("var x = 5; /* comentario */ var y = 10;"))
        self.assertEqual(len(tokens), 10)  # Asegurar que no se generen tokens extra

    def test_error_caracter(self):
        tokens = list(tokenize("@"))
        self.assertEqual(tokens, [Token("ERROR", "Caracter ilegal '@'", 1)])

    def test_error_comilla_no_cerrada(self):
        tokens = list(tokenize("'a"))
        self.assertEqual(tokens[0].type, "ERROR")
        self.assertEqual(tokens[0].value, 'Caracter no válido o no terminado "\'"')
        self.assertEqual(tokens[0].lineno, 1)
        # Verifica que se generen tokens adicionales después del error
        self.assertGreater(len(tokens), 1)

    def test_error_comentario_no_cerrado(self):
        tokens = list(tokenize("/* comentario sin cerrar"))
        self.assertEqual(tokens[0], Token("ERROR", "Comentario no terminado", 1))
        # Verifica que se generen tokens adicionales después del error
        self.assertGreater(len(tokens), 1)


if __name__ == "__main__":
    unittest.main()
