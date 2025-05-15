import unittest
import sys
import os

# Ajuste ruta para importar el lexer (asumiendo que lexer.py está en src/)
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from lexer import Token, tokenize

class TestLexer(unittest.TestCase):
    def _filter(self, tokens):
        # Filtra tokens tipo 'EOF' si los hubiera
        return [t for t in tokens if t.type != 'EOF']

    def test_palabras_reservadas(self):
        raw = 'const var print return break continue if else while func import true false'
        tokens = self._filter(list(tokenize(raw)))
        tipos = ['CONST','VAR','PRINT','RETURN','BREAK','CONTINUE','IF','ELSE','WHILE','FUNC','IMPORT','BOOL','BOOL']
        valores = ['const','var','print','return','break','continue','if','else','while','func','import','true','false']
        expected = [Token(tipos[i], valores[i], 1) for i in range(len(tipos))]
        self.assertEqual(tokens, expected)

    def test_identificadores(self):
        tokens = self._filter(list(tokenize('variable _var1 a1b2c3')))
        expected = [
            Token('ID', 'variable', 1),
            Token('ID', '_var1', 1),
            Token('ID', 'a1b2c3', 1),
        ]
        self.assertEqual(tokens, expected)

    def test_numeros(self):
        tokens = self._filter(list(tokenize('123 45.67 .456 123.')))
        expected = [
            Token('INTEGER', '123', 1),
            Token('FLOAT', '45.67', 1),
            Token('FLOAT', '.456', 1),
            Token('FLOAT', '123.', 1),
        ]
        self.assertEqual(tokens, expected)

    def test_operadores(self):
        tokens = self._filter(list(tokenize('+ - * / <= >= == != && || ^')))
        tipos = ['PLUS','MINUS','TIMES','DIVIDE','LE','GE','EQ','NE','LAND','LOR','GROW']
        valores = ['+','-','*','/','<=','>=','==','!=','&&','||','^']
        expected = [Token(tipos[i], valores[i], 1) for i in range(len(tipos))]
        self.assertEqual(tokens, expected)

    def test_simbolos_miscelaneos(self):
        tokens = self._filter(list(tokenize('= ; ( ) { } , `')))
        tipos = ['ASSIGN','SEMI','LPAREN','RPAREN','LBRACE','RBRACE','COMMA','DEREF']
        valores = ['=',';','(',')','{','}',',','`']
        expected = [Token(tipos[i], valores[i], 1) for i in range(len(tipos))]
        self.assertEqual(tokens, expected)

    def test_comentarios(self):
        tokens = self._filter(list(tokenize('var x = 5; // comentario')))
        expected = [
            Token('VAR', 'var', 1),
            Token('ID', 'x', 1),
            Token('ASSIGN', '=', 1),
            Token('INTEGER', '5', 1),
            Token('SEMI', ';', 1),
        ]
        self.assertEqual(tokens, expected)

    def test_comentario_bloque(self):
        tokens = self._filter(list(tokenize('var x = 5; /* comentario */ var y = 10;')))
        # 'var x = 5;' (5 tokens) + 'var y = 10;' (5 tokens)
        self.assertEqual(len(tokens), 10)

    def test_error_caracter(self):
        tokens = self._filter(list(tokenize('@')))
        self.assertEqual(tokens, [Token('ERROR', "Caracter ilegal '@'", 1)])

    def test_error_comilla_no_cerrada(self):
        tokens = self._filter(list(tokenize("'a")))
        self.assertTrue(tokens)
        self.assertEqual(tokens[0].type, 'ERROR')
        # Solo verificamos que contenga el mensaje base
        self.assertIn('Caracter no válido o no terminado', tokens[0].value)
        self.assertEqual(tokens[0].lineno, 1)

    def test_error_comentario_no_cerrado(self):
        tokens = self._filter(list(tokenize('/* comentario sin cerrar')))
        self.assertEqual(tokens[0], Token('ERROR', 'Comentario no terminado', 1))
        self.assertGreater(len(tokens), 1)

if __name__ == '__main__':
    unittest.main()
