import unittest
from tokenize_1 import tokenize, Token 

class TestLexer(unittest.TestCase):
    
    def test_palabras_reservadas(self):
        tokens = list(tokenize("const var print return break continue if else while func import true false"))
        palabras = ["CONST", "VAR", "PRINT", "RETURN", "BREAK", "CONTINUE", "IF", "ELSE", "WHILE", "FUNC", "IMPORT", "TRUE", "FALSE"]
        valores = ["const", "var", "print", "return", "break", "continue", "if", "else", "while", "func", "import", "true", "false"]
        for i, token in enumerate(tokens):
            self.assertEqual(token, Token(palabras[i], valores[i], 1))
    
    def test_identificadores(self):
        tokens = list(tokenize("variable _var1 a1b2c3"))
        self.assertEqual(tokens[0], Token("ID", "variable", 1))
        self.assertEqual(tokens[1], Token("ID", "_var1", 1))
        self.assertEqual(tokens[2], Token("ID", "a1b2c3", 1))
    
    def test_numeros(self):
        tokens = list(tokenize("123 45.67 .456 123."))
        self.assertEqual(tokens[0], Token("INTEGER", "123", 1))
        self.assertEqual(tokens[1], Token("FLOAT", "45.67", 1))
        self.assertEqual(tokens[2], Token("FLOAT", ".456", 1))
        self.assertEqual(tokens[3], Token("FLOAT", "123.", 1))
    
    def test_operadores(self):
        tokens = list(tokenize("+ - * / <= >= == != && || ^"))
        tipos = ["PLUS", "MINUS", "TIMES", "DIVIDE", "LE", "GE", "EQ", "NE", "LAND", "LOR", "GROW"]
        valores = ["+", "-", "*", "/", "<=", ">=", "==", "!=", "&&", "||", "^"]
        for i, token in enumerate(tokens):
            self.assertEqual(token, Token(tipos[i], valores[i], 1))
    
    def test_simbolos_miscelaneos(self):
        tokens = list(tokenize("= ; ( ) { } , `"))
        tipos = ["ASSIGN", "SEMI", "LPAREN", "RPAREN", "LBRACE", "RBRACE", "COMMA", "DEREF"]
        valores = ["=", ";", "(", ")", "{", "}", ",", "`"]
        for i, token in enumerate(tokens):
            self.assertEqual(token, Token(tipos[i], valores[i], 1))
    
    def test_comentarios(self):
        tokens = list(tokenize("var x = 5; // comentario"))
        self.assertEqual(len(tokens), 5)
        self.assertEqual(tokens[0], Token("VAR", "var", 1))
        self.assertEqual(tokens[1], Token("ID", "x", 1))
        self.assertEqual(tokens[2], Token("ASSIGN", "=", 1))
        self.assertEqual(tokens[3], Token("INTEGER", "5", 1))
        self.assertEqual(tokens[4], Token("SEMI", ";", 1))
    
    def test_comentario_bloque(self):
        tokens = list(tokenize("var x = 5; /* comentario */ var y = 10;"))
        self.assertEqual(len(tokens), 10)
    
    def test_error_caracter(self):
        with self.assertRaises(ValueError):
            list(tokenize("@"))
    
    def test_error_comilla_no_cerrada(self):
        with self.assertRaises(ValueError):
            list(tokenize("'a"))
    
    def test_error_comentario_no_cerrado(self):
        with self.assertRaises(ValueError):
            list(tokenize("/* comentario sin cerrar"))
    
if __name__ == '__main__':
    unittest.main()
