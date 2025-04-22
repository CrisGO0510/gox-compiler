import unittest
import sys
import os

# Agregar ruta a src/
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from lexer import tokenize
from parser import RecursiveDescentParser
from check import Checker
from error import ErrorManager


class TestChecker(unittest.TestCase):

    def analizar(self, source: str):
        tokens = list(tokenize(source))
        parser = RecursiveDescentParser(tokens, 0)
        return parser.program()

    def setUp(self):
        ErrorManager._errorCount = 0

    def test_vardecl_sin_tipo_con_expr(self):
        code = "var x = 10;"
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_const_sin_expr(self):
        code = "const x int;"
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_asignacion_invalida(self):
        code = """
        var x int = 1;
        x = false;
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_if_no_bool(self):
        code = """
        var x int = 3;
        if x {
            print x;
        }
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_while_no_bool(self):
        code = """
        var y float = 3.14;
        while y {
            print y;
        }
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_return_tipo_incorrecto(self):
        code = """
        func hola() int {
            return true;
        }
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_funcion_sin_return(self):
        code = """
        func faltaRetorno() int {
            print 10;
        }
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)

    def test_funcion_argumentos_invalidos(self):
        code = """
            func prueba(hola int) int {
                var x int = 3;
                return hola + x;
            }

            func main() int {
                var y int = 5;
                print prueba(y, 10);
                return 0;
            }
        """
        Checker.check(self.analizar(code))
        self.assertEqual(ErrorManager._errorCount, 1)


if __name__ == "__main__":
    unittest.main()
