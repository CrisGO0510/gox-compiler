import unittest
from lexer import tokenize
from parser import RecursiveDescentParser
from check import Checker


class SemanticTests(unittest.TestCase):
    def test_variable_no_declarada(self):
        code = "x = 10;"
        tokens = list(tokenize(code))
        ast = RecursiveDescentParser(tokens, 0).program()
        with self.assertRaises(NameError):
            Checker.check(ast)

    def test_const_modificada(self):
        code = "const x int = 5; x = 7;"
        tokens = list(tokenize(code))  # ✅ CORREGIDO
        ast = RecursiveDescentParser(tokens, 0).program()
        with self.assertRaises(TypeError):
            Checker.check(ast)

    def test_return_incorrecto(self):
        code = "func f() int { return true; }"
        tokens = list(tokenize(code))  # ✅ CORREGIDO
        ast = RecursiveDescentParser(tokens, 0).program()
        with self.assertRaises(TypeError):
            Checker.check(ast)
    
    def test_llamada_funcion_argumentos_incorrectos(self):
        code = """
        func sumar(a int, b int) int {
            return a + b;
        }

        func main() int {
            var x int;
            x = sumar(5);  // falta un argumento
            return x;
        }
        """
        tokens = list(tokenize(code))
        ast = RecursiveDescentParser(tokens, 0).program()
        with self.assertRaises(TypeError) as cm:
            Checker.check(ast)
        self.assertIn("Número incorrecto de argumentos", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
