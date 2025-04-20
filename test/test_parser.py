import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from parser import RecursiveDescentParser, Program, Vardecl, FuncDecl
from lexer import Token


class TestParser(unittest.TestCase):

    def test_variable_declaration(self):
        tokens = [
            Token("VAR", "var", 1),
            Token("ID", "x", 1),
            Token("TYPE", "int", 1),
            Token("ASSIGN", "=", 1),
            Token("INTEGER", "10", 1),
            Token("SEMI", ";", 1),
            Token("EOF", "", 2),
        ]

        parser = RecursiveDescentParser(tokens, 0)
        program = parser.program()

        self.assertIsInstance(program, Program)
        self.assertEqual(len(program.statements), 1)

        stmt = program.statements[0]
        self.assertIsInstance(stmt, Vardecl)
        self.assertEqual(stmt.id, "x")
        self.assertEqual(stmt.type, "int")
        self.assertEqual(stmt.assignment, "=")
        self.assertEqual(
            stmt.expression.orterm.andterm.relTerm.addTerm.factor.literal, "10"
        )

    def test_empty_function(self):
        tokens = [
            Token("FUNC", "func", 1),
            Token("ID", "main", 1),
            Token("LPAREN", "(", 1),
            Token("RPAREN", ")", 1),
            Token("TYPE", "int", 1),
            Token("LBRACE", "{", 1),
            Token("RBRACE", "}", 2),
            Token("EOF", "", 3),
        ]

        parser = RecursiveDescentParser(tokens, 0)
        program = parser.program()

        self.assertEqual(len(program.statements), 1)
        self.assertIsInstance(program.statements[0], FuncDecl)
        self.assertEqual(program.statements[0].id, "main")
        self.assertEqual(program.statements[0].return_type, "int")
        self.assertEqual(len(program.statements[0].statements), 0)


if __name__ == "__main__":
    unittest.main()
