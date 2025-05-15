import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from ircode import IRModule, IRGlobal, IRInstruction, IRFunction, IRType

class TestIRGlobal(unittest.TestCase):
    def test_dump_without_value(self):
        g = IRGlobal('x', 'int')
        self.assertEqual(g.dump(), 'GLOBAL::: x I')

    def test_dump_with_value(self):
        g = IRGlobal('y', 'float', 3.14)
        self.assertEqual(g.dump(), 'GLOBAL::: y F 3.14')

class TestIRType(unittest.TestCase):
    def test_getTypeMap_valid(self):
        self.assertEqual(IRType.getTypeMap('int'), 'I')
        self.assertEqual(IRType.getTypeMap('float'), 'F')
        self.assertEqual(IRType.getTypeMap('bool'), 'B')
        self.assertEqual(IRType.getTypeMap('char'), 'C')

    def test_getTypeMap_invalid(self):
        with self.assertRaises(Exception):
            IRType.getTypeMap('string')

    def test_getTypeMapInv(self):
        self.assertEqual(IRType.getTypeMapInv('I'), 'int')
        self.assertEqual(IRType.getTypeMapInv('F'), 'float')
        with self.assertRaises(Exception):
            IRType.getTypeMapInv('X')

    def test_getConst(self):
        # El método getConst agrega 'CONST' + mapa de tipo
        self.assertEqual(IRType.getConst('int'), 'CONSTI')
        self.assertEqual(IRType.getConst('bool'), 'CONSTB')
        with self.assertRaises(Exception):
            IRType.getConst('string')

    def test_getPrint(self):
        self.assertEqual(IRType.getPrint('int'), 'PRINTI')
        self.assertEqual(IRType.getPrint('I'), 'PRINTI')
        with self.assertRaises(Exception):
            IRType.getPrint('X')

    def test_getBinOpCode(self):
        # Usando código de tipo
        self.assertEqual(IRType.getBinOpCode('I', '+'), 'ADDI')
        self.assertEqual(IRType.getBinOpCode('F', '*'), 'MULF')
        # Usando nombre completo de tipo
        self.assertEqual(IRType.getBinOpCode('int', '+'), 'ADDI')
        with self.assertRaises(Exception):
            IRType.getBinOpCode('I', '%')

class TestIRFunction(unittest.TestCase):
    def test_ir_function_dump(self):
        mod = IRModule()
        f = IRFunction(mod, 'foo', ['a'], ['int'], 'bool')
        # Añadir variables locales con tipos char y float
        f.locals = {'x': 'char', 'y': 'float'}
        # Añadir instrucciones de ejemplo
        f.code = [IRInstruction('CONSTI', 42), IRInstruction('PRINTI')]
        dump = f.dump()
        self.assertIn('FUNCTION::: foo', dump)
        self.assertIn("'x': 'C'", dump)
        self.assertIn("'y': 'F'", dump)
        self.assertIn("('CONSTI', 42)", dump)
        self.assertIn("('PRINTI',)", dump)

class TestIRModule(unittest.TestCase):
    def test_ir_module_dump(self):
        mod = IRModule()
        # Agregar un global y una función con RET
        mod.globals['x'] = IRGlobal('x', 'int', 10)
        f = IRFunction(mod, 'foo', [], [], 'int')
        f.code = [IRInstruction('RET')]
        dump = mod.dump()
        self.assertTrue(dump.startswith('MODULE:::'))
        self.assertIn('GLOBAL::: x I 10', dump)
        self.assertIn('FUNCTION::: foo', dump)

if __name__ == '__main__':
    unittest.main()
